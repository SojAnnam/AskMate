--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.7
-- Dumped by pg_dump version 9.5.7

-- Started on 2017-06-06 14:20:26 CEST

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
-- TOC entry 198 (class 1259 OID 33223)
-- Name: user_attributes; Type: TABLE; Schema: public; Owner: markorkenyi
--

CREATE TABLE user_attributes (
    user_id integer NOT NULL,
    question_id integer,
    answer_id integer,
    comment_id integer
);


ALTER TABLE user_attributes OWNER TO markorkenyi;

--
-- TOC entry 2185 (class 0 OID 33223)
-- Dependencies: 198
-- Data for Name: user_attributes; Type: TABLE DATA; Schema: public; Owner: markorkenyi
--

COPY user_attributes (user_id, question_id, answer_id, comment_id) FROM stdin;
\.


--
-- TOC entry 2069 (class 2606 OID 33236)
-- Name: answer_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY user_attributes
    ADD CONSTRAINT answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);


--
-- TOC entry 2070 (class 2606 OID 33241)
-- Name: comment_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY user_attributes
    ADD CONSTRAINT comment_id FOREIGN KEY (comment_id) REFERENCES comment(id);


--
-- TOC entry 2068 (class 2606 OID 33231)
-- Name: question_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY user_attributes
    ADD CONSTRAINT question_id FOREIGN KEY (question_id) REFERENCES question(id);


--
-- TOC entry 2067 (class 2606 OID 33226)
-- Name: user_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY user_attributes
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES users(id);


-- Completed on 2017-06-06 14:20:26 CEST

--
-- PostgreSQL database dump complete
--

