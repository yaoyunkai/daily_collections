--
-- PostgreSQL database dump
--

\restrict XOC6kuSBwc5avTXxVvoFnV6EEjUKefnH3qyGirGK4d9sZmPiznZNxO5nijC7NIR

-- Dumped from database version 16.13
-- Dumped by pg_dump version 16.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dummy_article; Type: TABLE; Schema: public; Owner: test1
--

CREATE TABLE public.dummy_article (
    id integer NOT NULL,
    title character varying(50) NOT NULL,
    content text,
    tags character varying(20)[] DEFAULT '{}'::character varying[] NOT NULL
);


ALTER TABLE public.dummy_article OWNER TO test1;

--
-- Name: dummy_article_id_seq; Type: SEQUENCE; Schema: public; Owner: test1
--

CREATE SEQUENCE public.dummy_article_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dummy_article_id_seq OWNER TO test1;

--
-- Name: dummy_article_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: test1
--

ALTER SEQUENCE public.dummy_article_id_seq OWNED BY public.dummy_article.id;


--
-- Name: person; Type: TABLE; Schema: public; Owner: test1
--

CREATE TABLE public.person (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    gender character varying(1) DEFAULT 'N'::character varying NOT NULL,
    birthday date,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.person OWNER TO test1;

--
-- Name: COLUMN person.gender; Type: COMMENT; Schema: public; Owner: test1
--

COMMENT ON COLUMN public.person.gender IS '性别字段
N 未知
M 男
W 女';


--
-- Name: person_id_seq; Type: SEQUENCE; Schema: public; Owner: test1
--

CREATE SEQUENCE public.person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER SEQUENCE public.person_id_seq OWNER TO test1;

--
-- Name: person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: test1
--

ALTER SEQUENCE public.person_id_seq OWNED BY public.person.id;


--
-- Name: post; Type: TABLE; Schema: public; Owner: test1
--

CREATE TABLE public.post (
    id integer NOT NULL,
    person_id integer,
    title character varying(60) NOT NULL,
    content text NOT NULL,
    status character varying(1) DEFAULT 'S'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.post OWNER TO test1;

--
-- Name: TABLE post; Type: COMMENT; Schema: public; Owner: test1
--

COMMENT ON TABLE public.post IS '发表的文章';


--
-- Name: COLUMN post.title; Type: COMMENT; Schema: public; Owner: test1
--

COMMENT ON COLUMN public.post.title IS '文章标题';


--
-- Name: COLUMN post.status; Type: COMMENT; Schema: public; Owner: test1
--

COMMENT ON COLUMN public.post.status IS '文章的状态
S 草稿状态
T 待审核
D 审核完成';


--
-- Name: post_id_seq; Type: SEQUENCE; Schema: public; Owner: test1
--

CREATE SEQUENCE public.post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER SEQUENCE public.post_id_seq OWNER TO test1;

--
-- Name: post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: test1
--

ALTER SEQUENCE public.post_id_seq OWNED BY public.post.id;


--
-- Name: dummy_article id; Type: DEFAULT; Schema: public; Owner: test1
--

ALTER TABLE ONLY public.dummy_article ALTER COLUMN id SET DEFAULT nextval('public.dummy_article_id_seq'::regclass);


--
-- Name: person id; Type: DEFAULT; Schema: public; Owner: test1
--

ALTER TABLE ONLY public.person ALTER COLUMN id SET DEFAULT nextval('public.person_id_seq'::regclass);


--
-- Name: post id; Type: DEFAULT; Schema: public; Owner: test1
--

ALTER TABLE ONLY public.post ALTER COLUMN id SET DEFAULT nextval('public.post_id_seq'::regclass);


--
-- Name: dummy_article dummy_article_pkey; Type: CONSTRAINT; Schema: public; Owner: test1
--

ALTER TABLE ONLY public.dummy_article
    ADD CONSTRAINT dummy_article_pkey PRIMARY KEY (id);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: test1
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- Name: post post_pkey; Type: CONSTRAINT; Schema: public; Owner: test1
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- Name: ix_dummy_article_tags; Type: INDEX; Schema: public; Owner: test1
--

CREATE INDEX ix_dummy_article_tags ON public.dummy_article USING gin (tags) WITH (fastupdate='true');


--
-- Name: post fk_post_person; Type: FK CONSTRAINT; Schema: public; Owner: test1
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT fk_post_person FOREIGN KEY (person_id) REFERENCES public.person(id);


--
-- PostgreSQL database dump complete
--

\unrestrict XOC6kuSBwc5avTXxVvoFnV6EEjUKefnH3qyGirGK4d9sZmPiznZNxO5nijC7NIR

