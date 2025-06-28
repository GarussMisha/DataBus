CREATE TABLE IF NOT EXISTS countries (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    create_dt TIMESTAMP DEFAULT NOW()
);

-- 1. Создание таблицы для логирования изменений в таблице countries
CREATE TABLE IF NOT EXISTS countries_log (
    log_id serial PRIMARY KEY,
    operation_type varchar(10) NOT NULL, -- INSERT, UPDATE, DELETE
    old_data jsonb,
    new_data jsonb,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- 2. Создание триггерной функции
CREATE OR REPLACE FUNCTION log_countries_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO countries_log (operation_type, new_data)
        VALUES (TG_OP, to_jsonb(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO countries_log (operation_type, old_data, new_data)
        VALUES (TG_OP, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO countries_log (operation_type, old_data)
        VALUES (TG_OP, to_jsonb(OLD));
        RETURN OLD;
    END IF;
    RETURN NULL; -- Результат игнорируется, так как это AFTER триггер
END;
$$ LANGUAGE plpgsql;

-- 3. Создание триггера для таблицы countries
-- Удаляем старый триггер, если он существует, чтобы избежать дублирования
DROP TRIGGER IF EXISTS countries_after_change_trigger ON countries;

CREATE TRIGGER countries_after_change_trigger
AFTER INSERT OR UPDATE OR DELETE ON countries
FOR EACH ROW
EXECUTE FUNCTION log_countries_changes();
