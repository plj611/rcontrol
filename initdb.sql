CREATE DATABASE devrcontrol;
CREATE ROLE allperm;
\c devrcontrol
GRANT USAGE, CREATE ON SCHEMA public to allperm;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA PUBLIC TO allperm;
ALTER DEFAULT PRIVILEGES IN SCHEMA public  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO allperm;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO allperm;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO allperm;
CREATE USER pl704206 WITH PASSWORD 'phm123';
GRANT allperm TO pl704206;