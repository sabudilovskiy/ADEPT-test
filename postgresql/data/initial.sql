-- Вставка типов
INSERT INTO objects.types (name) VALUES 
('Город'),         -- Тип с кириллическим именем
('River'),         -- Тип с латинским именем
('_Mountain'),     -- Тип с именем, начинающимся с нестандартного символа
('Forest'),        
('Озеро'),         -- Тип с кириллическим именем
('Valley'),        
('Лесопарк'),      -- Тип с кириллическим именем
('Остров'),        -- Тип с кириллическим именем
('@HistoricalSite'), -- Тип с нестандартным символом
('Крепость'),      -- Тип с кириллическим именем
('Desert'),        
('Swamp');        

-- Получение type_id для вставки объектов
WITH type_ids AS (
    SELECT type_id FROM objects.types WHERE name IN 
    ('Город', 'River', '_Mountain', 'Forest', 'Озеро', 'Valley', 'Лесопарк', 'Остров', '@HistoricalSite', 'Крепость', 'Desert', 'Swamp')
)
SELECT * FROM type_ids;

-- Вставка объектов
INSERT INTO objects.objects (name, type_id, coordinates, created_at, token) VALUES 
-- Тип 'Город'
('Москва', (SELECT type_id FROM objects.types WHERE name = 'Город'), ROW(55.7558, 37.6173), '2024-01-01T10:00:00Z', uuid_generate_v4()),
('Санкт-Петербург', (SELECT type_id FROM objects.types WHERE name = 'Город'), ROW(59.9343, 30.3351), '2024-02-15T11:30:00Z', uuid_generate_v4()),
('Екатеринбург', (SELECT type_id FROM objects.types WHERE name = 'Город'), ROW(56.8389, 60.6057), '2023-06-05T09:45:00Z', uuid_generate_v4()),
('Казань', (SELECT type_id FROM objects.types WHERE name = 'Город'), ROW(55.7940, 49.1067), '2024-08-22T14:00:00Z', uuid_generate_v4()),
('Новосибирск', (SELECT type_id FROM objects.types WHERE name = 'Город'), ROW(55.0084, 82.9357), '2024-12-25T16:30:00Z', uuid_generate_v4()),

-- Тип 'River'
('Nile', (SELECT type_id FROM objects.types WHERE name = 'River'), ROW(30.0444, 31.2357), '2024-03-10T12:00:00Z', uuid_generate_v4()),
('Amazon', (SELECT type_id FROM objects.types WHERE name = 'River'), ROW(-3.4653, -62.2159), '2023-07-18T15:20:00Z', uuid_generate_v4()),
('Volga', (SELECT type_id FROM objects.types WHERE name = 'River'), ROW(48.7194, 44.5018), '2024-05-25T08:15:00Z', uuid_generate_v4()),
('Yangtze', (SELECT type_id FROM objects.types WHERE name = 'River'), ROW(31.2304, 121.4737), '2024-09-14T19:45:00Z', uuid_generate_v4()),
('Thames', (SELECT type_id FROM objects.types WHERE name = 'River'), ROW(51.5074, -0.1278), '2024-01-30T20:30:00Z', uuid_generate_v4()),

-- Тип '_Mountain'
('_Everest', (SELECT type_id FROM objects.types WHERE name = '_Mountain'), ROW(27.9881, 86.9250), '2024-09-01T07:00:00Z', uuid_generate_v4()),
('_K2', (SELECT type_id FROM objects.types WHERE name = '_Mountain'), ROW(35.8818, 76.5133), '2023-12-12T13:40:00Z', uuid_generate_v4()),
('_Kangchenjunga', (SELECT type_id FROM objects.types WHERE name = '_Mountain'), ROW(27.7025, 88.1475), '2024-05-06T22:50:00Z', uuid_generate_v4()),
('_Lhotse', (SELECT type_id FROM objects.types WHERE name = '_Mountain'), ROW(27.9617, 86.9330), '2024-07-19T06:10:00Z', uuid_generate_v4()),
('_Makalu', (SELECT type_id FROM objects.types WHERE name = '_Mountain'), ROW(27.8897, 87.0883), '2024-10-29T09:55:00Z', uuid_generate_v4()),

-- Тип 'Forest'
('Sherwood', (SELECT type_id FROM objects.types WHERE name = 'Forest'), ROW(53.2516, -1.0763), '2024-09-03T11:11:11Z', uuid_generate_v4()),
('BlackForest', (SELECT type_id FROM objects.types WHERE name = 'Forest'), ROW(48.0974, 8.2441), '2023-01-11T22:22:22Z', uuid_generate_v4()),
('AmazonRainforest', (SELECT type_id FROM objects.types WHERE name = 'Forest'), ROW(-3.4653, -62.2159), '2024-07-07T07:07:07Z', uuid_generate_v4()),
('BiałowieżaForest', (SELECT type_id FROM objects.types WHERE name = 'Forest'), ROW(52.7443, 23.8708), '2024-09-09T09:09:09Z', uuid_generate_v4()),

-- Тип 'Озеро'
('Байкал', (SELECT type_id FROM objects.types WHERE name = 'Озеро'), ROW(53.5587, 108.1650), '2024-03-03T03:33:33Z', uuid_generate_v4()),
('Ладога', (SELECT type_id FROM objects.types WHERE name = 'Озеро'), ROW(60.7500, 31.5000), '2024-09-02T02:22:22Z', uuid_generate_v4()),
('Онега', (SELECT type_id FROM objects.types WHERE name = 'Озеро'), ROW(61.8333, 35.0000), '2023-04-04T04:44:44Z', uuid_generate_v4()),
('Ильмень', (SELECT type_id FROM objects.types WHERE name = 'Озеро'), ROW(58.2170, 31.4167), '2024-05-05T05:55:55Z', uuid_generate_v4()),

-- Тип 'Valley'
('DeathValley', (SELECT type_id FROM objects.types WHERE name = 'Valley'), ROW(36.5323, -116.9325), '2024-08-08T08:08:08Z', uuid_generate_v4()),
('RiftValley', (SELECT type_id FROM objects.types WHERE name = 'Valley'), ROW(-3.3762, 36.8555), '2023-09-09T09:09:09Z', uuid_generate_v4()),
('YosemiteValley', (SELECT type_id FROM objects.types WHERE name = 'Valley'), ROW(37.7335, -119.6652), '2024-06-06T06:06:06Z', uuid_generate_v4()),

-- Тип 'Лесопарк'
('Лосиний Остров', (SELECT type_id FROM objects.types WHERE name = 'Лесопарк'), ROW(55.8333, 37.7500), '2024-01-01T01:01:01Z', uuid_generate_v4()),
('Сокольники', (SELECT type_id FROM objects.types WHERE name = 'Лесопарк'), ROW(55.7973, 37.6786), '2023-02-02T02:02:02Z', uuid_generate_v4()),

-- Тип 'Остров'
('Сахалин', (SELECT type_id FROM objects.types WHERE name = 'Остров'), ROW(50.6947, 142.2019), '2024-03-03T03:03:03Z', uuid_generate_v4()),
('Кунашир', (SELECT type_id FROM objects.types WHERE name = 'Остров'), ROW(44.2683, 146.0292), '2024-04-04T04:04:04Z', uuid_generate_v4()),

-- Тип '@HistoricalSite'
('@Stonehenge', (SELECT type_id FROM objects.types WHERE name = '@HistoricalSite'), ROW(51.1789, -1.8262), '2023-12-12T12:12:12Z', uuid_generate_v4()),

-- Тип 'Крепость'
('Кремль', (SELECT type_id FROM objects.types WHERE name = 'Крепость'), ROW(55.7520, 37.6175), '2024-03-03T03:03:03Z', uuid_generate_v4()),

-- Тип 'Desert'
('Sahara', (SELECT type_id FROM objects.types WHERE name = 'Desert'), ROW(8023.4162, 3500.6628), '2024-11-11T11:11:11Z', uuid_generate_v4()),

-- Тип 'Swamp'
('Everglades', (SELECT type_id FROM objects.types WHERE name = 'Swamp'), ROW(1000.7683, -8000.2057), '2024-12-12T12:12:12Z', uuid_generate_v4());
