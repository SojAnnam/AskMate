--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.7
-- Dumped by pg_dump version 9.5.7

-- Started on 2017-06-07 11:36:03 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12395)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2223 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 187 (class 1259 OID 33155)
-- Name: answer; Type: TABLE; Schema: public; Owner: markorkenyi
--

CREATE TABLE answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text
);


ALTER TABLE answer OWNER TO markorkenyi;

--
-- TOC entry 186 (class 1259 OID 33153)
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: markorkenyi
--

CREATE SEQUENCE answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE answer_id_seq OWNER TO markorkenyi;

--
-- TOC entry 2224 (class 0 OID 0)
-- Dependencies: 186
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: markorkenyi
--

ALTER SEQUENCE answer_id_seq OWNED BY answer.id;


--
-- TOC entry 181 (class 1259 OID 33098)
-- Name: applicants_id_seq; Type: SEQUENCE; Schema: public; Owner: markorkenyi
--

CREATE SEQUENCE applicants_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE applicants_id_seq OWNER TO markorkenyi;

--
-- TOC entry 189 (class 1259 OID 33164)
-- Name: comment; Type: TABLE; Schema: public; Owner: markorkenyi
--

CREATE TABLE comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer
);


ALTER TABLE comment OWNER TO markorkenyi;

--
-- TOC entry 188 (class 1259 OID 33162)
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: markorkenyi
--

CREATE SEQUENCE comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comment_id_seq OWNER TO markorkenyi;

--
-- TOC entry 2225 (class 0 OID 0)
-- Dependencies: 188
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: markorkenyi
--

ALTER SEQUENCE comment_id_seq OWNED BY comment.id;


--
-- TOC entry 182 (class 1259 OID 33106)
-- Name: mentors_id_seq; Type: SEQUENCE; Schema: public; Owner: markorkenyi
--

CREATE SEQUENCE mentors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mentors_id_seq OWNER TO markorkenyi;

--
-- TOC entry 185 (class 1259 OID 33146)
-- Name: question; Type: TABLE; Schema: public; Owner: markorkenyi
--

CREATE TABLE question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text
);


ALTER TABLE question OWNER TO markorkenyi;

--
-- TOC entry 184 (class 1259 OID 33144)
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: markorkenyi
--

CREATE SEQUENCE question_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE question_id_seq OWNER TO markorkenyi;

--
-- TOC entry 2226 (class 0 OID 0)
-- Dependencies: 184
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: markorkenyi
--

ALTER SEQUENCE question_id_seq OWNED BY question.id;


--
-- TOC entry 190 (class 1259 OID 33171)
-- Name: question_tag; Type: TABLE; Schema: public; Owner: markorkenyi
--

CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE question_tag OWNER TO markorkenyi;

--
-- TOC entry 183 (class 1259 OID 33114)
-- Name: schools_id_seq; Type: SEQUENCE; Schema: public; Owner: markorkenyi
--

CREATE SEQUENCE schools_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE schools_id_seq OWNER TO markorkenyi;

--
-- TOC entry 192 (class 1259 OID 33176)
-- Name: tag; Type: TABLE; Schema: public; Owner: markorkenyi
--

CREATE TABLE tag (
    id integer NOT NULL,
    name text
);


ALTER TABLE tag OWNER TO markorkenyi;

--
-- TOC entry 191 (class 1259 OID 33174)
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: markorkenyi
--

CREATE SEQUENCE tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tag_id_seq OWNER TO markorkenyi;

--
-- TOC entry 2227 (class 0 OID 0)
-- Dependencies: 191
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: markorkenyi
--

ALTER SEQUENCE tag_id_seq OWNED BY tag.id;


--
-- TOC entry 194 (class 1259 OID 33223)
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
-- TOC entry 195 (class 1259 OID 33247)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: markorkenyi
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO markorkenyi;

--
-- TOC entry 193 (class 1259 OID 33218)
-- Name: users; Type: TABLE; Schema: public; Owner: markorkenyi
--

CREATE TABLE users (
    id integer DEFAULT nextval('users_id_seq'::regclass) NOT NULL,
    username character varying(128) NOT NULL,
    date date NOT NULL
);


ALTER TABLE users OWNER TO markorkenyi;

--
-- TOC entry 2062 (class 2604 OID 33158)
-- Name: id; Type: DEFAULT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY answer ALTER COLUMN id SET DEFAULT nextval('answer_id_seq'::regclass);


--
-- TOC entry 2063 (class 2604 OID 33167)
-- Name: id; Type: DEFAULT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY comment ALTER COLUMN id SET DEFAULT nextval('comment_id_seq'::regclass);


--
-- TOC entry 2061 (class 2604 OID 33149)
-- Name: id; Type: DEFAULT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY question ALTER COLUMN id SET DEFAULT nextval('question_id_seq'::regclass);


--
-- TOC entry 2064 (class 2604 OID 33179)
-- Name: id; Type: DEFAULT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY tag ALTER COLUMN id SET DEFAULT nextval('tag_id_seq'::regclass);


--
-- TOC entry 2207 (class 0 OID 33155)
-- Dependencies: 187
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: markorkenyi
--

COPY answer (id, submission_time, vote_number, question_id, message, image) FROM stdin;
1	2017-04-28 16:49:00	4	1	You need to use brackets: my_list = []	\N
2	2017-04-25 14:42:00	35	1	Look it up in the Python docs	images/image2.jpg
\.


--
-- TOC entry 2228 (class 0 OID 0)
-- Dependencies: 186
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: markorkenyi
--

SELECT pg_catalog.setval('answer_id_seq', 2, true);


--
-- TOC entry 2229 (class 0 OID 0)
-- Dependencies: 181
-- Name: applicants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: markorkenyi
--

SELECT pg_catalog.setval('applicants_id_seq', 10, true);


--
-- TOC entry 2209 (class 0 OID 33164)
-- Dependencies: 189
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: markorkenyi
--

COPY comment (id, question_id, answer_id, message, submission_time, edited_count) FROM stdin;
1	0	\N	Please clarify the question as it is too vague!	2017-05-01 05:49:00	\N
2	\N	1	I think you could use my_list = list() as well.	2017-05-02 16:55:00	\N
\.


--
-- TOC entry 2230 (class 0 OID 0)
-- Dependencies: 188
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: markorkenyi
--

SELECT pg_catalog.setval('comment_id_seq', 2, true);


--
-- TOC entry 2231 (class 0 OID 0)
-- Dependencies: 182
-- Name: mentors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: markorkenyi
--

SELECT pg_catalog.setval('mentors_id_seq', 22, true);


--
-- TOC entry 2205 (class 0 OID 33146)
-- Dependencies: 185
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: markorkenyi
--

COPY question (id, submission_time, view_number, vote_number, title, message, image) FROM stdin;
1	2017-04-29 09:19:00	15	9	Wordpress loading multiple jQuery Versions	I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();\n\nI could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.\n\nBUT in my theme i also using jquery via webpack so the loading order is now following:\n\njquery\nbooklet\napp.js (bundled file with webpack, including jquery)	images/image1.png
2	2017-05-01 10:41:00	1364	57	Drawing canvas with an image picked with Cordova Camera Plugin	I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS, it throws errors such as cross origin issue, or that I'm trying to use an unknown format.\n	\N
0	2017-04-28 08:29:00	30	7	How to make lists in Python?	I am totally new to this, any hints?	\N
\.


--
-- TOC entry 2232 (class 0 OID 0)
-- Dependencies: 184
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: markorkenyi
--

SELECT pg_catalog.setval('question_id_seq', 2, true);


--
-- TOC entry 2210 (class 0 OID 33171)
-- Dependencies: 190
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: markorkenyi
--

COPY question_tag (question_id, tag_id) FROM stdin;
0	1
1	3
2	3
\.


--
-- TOC entry 2233 (class 0 OID 0)
-- Dependencies: 183
-- Name: schools_id_seq; Type: SEQUENCE SET; Schema: public; Owner: markorkenyi
--

SELECT pg_catalog.setval('schools_id_seq', 4, true);


--
-- TOC entry 2212 (class 0 OID 33176)
-- Dependencies: 192
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: markorkenyi
--

COPY tag (id, name) FROM stdin;
1	python
2	sql
3	css
\.


--
-- TOC entry 2234 (class 0 OID 0)
-- Dependencies: 191
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: markorkenyi
--

SELECT pg_catalog.setval('tag_id_seq', 3, true);


--
-- TOC entry 2214 (class 0 OID 33223)
-- Dependencies: 194
-- Data for Name: user_attributes; Type: TABLE DATA; Schema: public; Owner: markorkenyi
--

COPY user_attributes (user_id, question_id, answer_id, comment_id) FROM stdin;
\.


--
-- TOC entry 2213 (class 0 OID 33218)
-- Dependencies: 193
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: markorkenyi
--

COPY users (id, username, date) FROM stdin;
7	Admin	2017-06-07
\.


--
-- TOC entry 2235 (class 0 OID 0)
-- Dependencies: 195
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: markorkenyi
--

SELECT pg_catalog.setval('users_id_seq', 8, true);


--
-- TOC entry 2077 (class 2606 OID 33222)
-- Name: id; Type: CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY users
    ADD CONSTRAINT id PRIMARY KEY (id);


--
-- TOC entry 2069 (class 2606 OID 33184)
-- Name: pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- TOC entry 2071 (class 2606 OID 33186)
-- Name: pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- TOC entry 2067 (class 2606 OID 33188)
-- Name: pk_question_id; Type: CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- TOC entry 2073 (class 2606 OID 33190)
-- Name: pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- TOC entry 2075 (class 2606 OID 33192)
-- Name: pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- TOC entry 2085 (class 2606 OID 33236)
-- Name: answer_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY user_attributes
    ADD CONSTRAINT answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);


--
-- TOC entry 2086 (class 2606 OID 33241)
-- Name: comment_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY user_attributes
    ADD CONSTRAINT comment_id FOREIGN KEY (comment_id) REFERENCES comment(id);


--
-- TOC entry 2079 (class 2606 OID 33193)
-- Name: fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);


--
-- TOC entry 2078 (class 2606 OID 33198)
-- Name: fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);


--
-- TOC entry 2081 (class 2606 OID 33203)
-- Name: fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);


--
-- TOC entry 2080 (class 2606 OID 33208)
-- Name: fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);


--
-- TOC entry 2082 (class 2606 OID 33213)
-- Name: fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);


--
-- TOC entry 2084 (class 2606 OID 33231)
-- Name: question_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY user_attributes
    ADD CONSTRAINT question_id FOREIGN KEY (question_id) REFERENCES question(id);


--
-- TOC entry 2083 (class 2606 OID 33226)
-- Name: user_id; Type: FK CONSTRAINT; Schema: public; Owner: markorkenyi
--

ALTER TABLE ONLY user_attributes
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES users(id);


--
-- TOC entry 2222 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2017-06-07 11:36:03 CEST

--
-- PostgreSQL database dump complete
--

