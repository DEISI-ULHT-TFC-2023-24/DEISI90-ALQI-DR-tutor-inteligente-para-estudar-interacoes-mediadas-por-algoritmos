-- Check if news_source table exists
DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM   information_schema.tables
        WHERE  table_schema = 'public'
        AND    table_name = 'news_source'
    ) THEN
        -- Create news_source table
        CREATE TABLE news_source (
            source_id SERIAL PRIMARY KEY,
            source_url TEXT,
            source_trust_rating FLOAT,
            source_name TEXT
        );
    END IF;
END $$;

-- Check if news_category table exists
DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM   information_schema.tables
        WHERE  table_schema = 'public'
        AND    table_name = 'news_category'
    ) THEN
        -- Create news_category table
        CREATE TABLE news_category (
            category_label TEXT PRIMARY KEY,
            category_id TEXT,
            category_code TEXT
        );
    END IF;
END $$;

-- Check if news_content table exists
DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM   information_schema.tables
        WHERE  table_schema = 'public'
        AND    table_name = 'news_content'
    ) THEN
        -- Create news_content table
        CREATE TABLE news_content (
            content_id SERIAL PRIMARY KEY,
            content_source_id INT,
            content_headline TEXT UNIQUE,
            content_source TEXT,
            content_url TEXT,
            content_category TEXT,
            content_text TEXT,
            content_image TEXT,
            content_date TEXT,
            FOREIGN KEY (content_source_id) REFERENCES news_source(source_id),
            FOREIGN KEY (content_category) REFERENCES news_category(category_label)
        );
    END IF;
END $$;

-- Check if news_thread table exists
DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM   information_schema.tables
        WHERE  table_schema = 'public'
        AND    table_name = 'news_thread'
    ) THEN
        -- Create news_thread table
        CREATE TABLE news_thread (
            thread_id SERIAL PRIMARY KEY,
            content_id INT,
            thread_response TEXT,
            FOREIGN KEY (content_id) REFERENCES news_content(content_id)
        );
    END IF;
END $$;


-- Insert data into news_category table if not exists
INSERT INTO news_category (category_label, category_id, category_code)
SELECT *
FROM (VALUES
    ('ultimas', 'Ult', '001'),
    ('politica', 'PL', '002'),
    ('fama', 'Fm', '003'),
    ('mundo', 'MN', '004'),
    ('tech', 'Tech', '005'),
    ('lifestyle', 'Life', '006'),
    ('casa', 'Casa', '007'),
    ('auto', 'Auto', '008'),
    ('pais', 'Pais', '008'),
    ('casaMinuto', 'CasaM', '009'),
    ('desporto', 'Des', '010'),
    ('economia', 'Eco', '011'),
    ('cultura', 'Cul', '012'),
    ('autoMinuto', 'AutoM', '013'),
    ('videos', 'Vid', '014'),
    ('audios', 'Aud', '015')
) AS data (category_label, category_id, category_code)
WHERE NOT EXISTS (
    SELECT 1
    FROM news_category nc
    WHERE nc.category_label = data.category_label
);
-- Insert data into news_source table if not exists
INSERT INTO news_source (source_url, source_trust_rating, source_name)
SELECT *
FROM (VALUES
    ('https://www.rtp.pt/', 8, 'RTP'),
    ('https://www.noticiasaominuto.com/', 6, 'Noticias ao Minuto')
) AS data (source_url, source_trust_rating, source_name)
WHERE NOT EXISTS (
    SELECT 1
    FROM news_source ns
    WHERE ns.source_url = data.source_url
);



