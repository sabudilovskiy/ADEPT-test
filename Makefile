GENERATE_SQL_QUERIES_FLAGS ?= src/sql src/codegen sql sql

.PHONY: check-git-status
check-git-status:
	@echo "Checking if all files are committed to git..."
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "The following files are not committed:"; \
		git status --short; \
		echo "Please commit all changes and try again."; \
		git diff --color | cat; \
		exit 1; \
	else \
		echo "All files are committed to git."; \
	fi

.PHONY: add-eol
add-eol:
	@find $(P) -type f | while read file; do \
        if ! tail -c1 "$$file" | grep -q "^$$"; then \
            echo >> "$$file"; \
        fi \
    done

.PHONY: add-eol-root
add-eol-root:
	@find . -maxdepth 1 -type f | while read file; do \
		if ! tail -c1 "$$file" | grep -q "^$$"; then \
			echo >> "$$file"; \
		fi \
    done

.PHONY: instal-compiler
install-compiler:
	@if [ "$(compiler)" = "clang" ]; then \
            wget https://apt.llvm.org/llvm.sh; \
            chmod +x llvm.sh; \
            sudo ./llvm.sh $(version); \
            rm llvm.sh;\
    elif [ "$(compiler)" = "gcc" ]; then \
      	sudo apt install -y g++-$(version); \
      	sudo apt install -y gcc-$(version); \
  	else \
      echo "Unknown compiler" >&2; \
  	fi

.PHONY: instal-compiler
docker-install-compiler:
	@if [ "$(compiler)" = "clang" ]; then \
            wget https://apt.llvm.org/llvm.sh; \
            chmod +x llvm.sh; \
            ./llvm.sh $(version); \
            rm llvm.sh;\
    elif [ "$(compiler)" = "gcc" ]; then \
      	apt install -y g++-$(version); \
      	apt install -y gcc-$(version); \
  	else \
      echo "Unknown compiler" >&2; \
  	fi

.PHONY: find-cxx-compiler
find-cxx-compiler:
	@if [ "$(compiler)" = "clang" ]; then \
        echo "/usr/bin/clang++-$(version)"; \
      elif [ "$(compiler)" = "gcc" ]; then \
        echo "/usr/bin/g++-$(version)"; \
      else \
        echo "Unknown compiler" >&2; \
      fi

.PHONY: find-c-compiler
find-c-compiler:
	@if [ "$(compiler)" = "clang" ]; then \
        echo "/usr/bin/clang-$(version)"; \
      elif [ "$(compiler)" = "gcc" ]; then \
        echo "/usr/bin/gcc-$(version)"; \
      else \
        echo "Unknown compiler" >&2;  \
      fi

.PHONY: format
format:
	python3.10 scripts/format_includes.py library boost uopenapi checks
	find src -name '*pp' -type f | xargs clang-format-17 -i
	find service -name '*pp' -type f | xargs clang-format-17 -i
	make add-eol P=src
	make add-eol P=service
	make add-eol P=.github
	make add-eol P=configs
	make add-eol P=scripts
	make add-eol P=tests
	make add-eol-root

.PHONY: gen-queries
gen-queries:
	@python3 scripts/generate_sql_queries.py $(GENERATE_SQL_QUERIES_FLAGS)

.PHONY: build-debug
build-debug:
	cmake --build build_debug

.PHONY: build-release
build-release:
	cmake --build build_release

.PHONY: run
run:
	chmod +x build_release/service
	./build_release/service --config configs/static_config.yaml --config_vars configs/config_vars.yaml

.PHONY: get_all_so
get_all_so:
	rm -rf _so
	mkdir _so
	ldd build_release/service | grep "=>" | awk '{print $$3}' | xargs -I {} cp {} _so

.PHONY: tests
tests:
	build_debug/runtests-testsuite-service --service-logs-pretty -vv tests

.PHONY: build-docker
build-docker: build-release get_all_so
	sudo docker build -t adept_service:latest .
	rm -rf _so
	mkdir -p release
	sudo docker save -o release/adept_service.tar adept_service:latest

.PHONY: release
release: 
	sudo mkdir -p _tmp/container/configs
	sudo mkdir -p _tmp/container/cores
	sudo mkdir -p _tmp/container/pg_data
	sudo cp configs/config_vars.docker.yaml _tmp/container/configs/config_vars.yaml
	sudo cp configs/static_config.yaml _tmp/container/configs/static_config.yaml
	sudo cp docker-compose.yml _tmp/docker-compose.yml
	sudo tar -cf release/container.tar _tmp/
	sudo rm -rf _tmp


.PHONY: start-docker
start-docker:
	sudo rm -rf container/configs
	sudo mkdir container/configs
	sudo cp configs/config_vars.docker.yaml container/configs/config_vars.yaml
	sudo cp configs/static_config.yaml container/configs/static_config.yaml
	sudo docker-compose up
