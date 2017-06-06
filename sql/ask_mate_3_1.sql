--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.7
-- Dumped by pg_dump version 9.5.7

-- Started on 2017-06-06 14:20:16 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 197 (class 1259 OID 33218)
-- Name: users; Type: TABLE; Schema: public; Owner: markorkenyi
--

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(128) NOT NULL,
    date date NOT NULL
);


ALTER TABLE users OWNER TO markorkenyi;

--
-- TOC entry 2183 (class 0 OID 33218)
-- Dependencies: 197
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: markorkenyi
--

COPY users (id, username, date) FROM stdin;
1	markorkenyi	2017-06-05
\.


--
-- TOC entry 2068 (class 2606 OID 33222)
-- Name: id; Type: CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY users
    ADD CONSTRAINT id PRIMARY KEY (id);


-- Completed on 2017-06-06 14:20:16 CEST

--
-- PostgreSQL database dump complete
--

