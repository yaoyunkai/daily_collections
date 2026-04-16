--
-- PostgreSQL database dump
--

\restrict OOigdMfLZhNypb1SLToT7F1JafJtc0vhkjOTSJHaG5ezOrpA8wMH45CC2kUY4sO

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

--
-- Name: refresh_first_pass_flag(); Type: FUNCTION; Schema: public; Owner: test1
--

CREATE FUNCTION public.refresh_first_pass_flag() RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    WITH
    -- 步骤 1: 精准找出哪些"组"有新数据
    TouchedGroups AS (
        SELECT DISTINCT sernum, test_area
        FROM test_record
        WHERE first_pass_flag = -1
    ),
    -- 步骤 2: 把这些组内的 (所有数据) 重新按业务时间排序计算
    CalculatedFlags AS (
        SELECT
            d.id,
            CASE
                WHEN ROW_NUMBER() OVER (
                    PARTITION BY d.sernum, d.test_area
                    ORDER BY d.record_time ASC
                ) = 1 THEN 1
                ELSE 0
            END AS correct_flag
        FROM test_record d
        INNER JOIN TouchedGroups tg
            ON d.sernum = tg.sernum AND d.test_area = tg.test_area
    )
    -- 步骤 3: 智能更新回主表
    UPDATE test_record d
    SET first_pass_flag = c.correct_flag
    FROM CalculatedFlags c
    WHERE d.id = c.id
      -- 只更新状态发生变化的数据！
      -- 这不仅会把 -1 变成 1 或 0，还会把因为乱序导致算错的历史 1 自动纠正为 0
      AND d.first_pass_flag IS DISTINCT FROM c.correct_flag;
END;
$$;


ALTER FUNCTION public.refresh_first_pass_flag() OWNER TO test1;

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
-- Name: test_record; Type: TABLE; Schema: public; Owner: test1
--

CREATE TABLE public.test_record (
    id integer NOT NULL,
    record_time timestamp with time zone NOT NULL,
    sernum character varying(50) NOT NULL,
    uuttype character varying(50) NOT NULL,
    test_area character varying(20) NOT NULL,
    passfail character varying(1) NOT NULL,
    runtime integer DEFAULT 0 NOT NULL,
    test_fail character varying(50) DEFAULT ''::character varying NOT NULL,
    test_machine character varying(20) NOT NULL,
    test_container character varying(50) NOT NULL,
    test_mode character varying(10) DEFAULT 'PROD0'::character varying NOT NULL,
    deviation character varying(16) DEFAULT 'D000000'::character varying NOT NULL,
    testr1name character varying(50) DEFAULT NULL::character varying,
    testr1 character varying(50) DEFAULT NULL::character varying,
    testr2name character varying(50) DEFAULT NULL::character varying,
    testr2 character varying(50) DEFAULT NULL::character varying,
    testr3name character varying(50) DEFAULT NULL::character varying,
    testr3 character varying(50) DEFAULT NULL::character varying,
    first_pass_flag smallint DEFAULT '-1'::integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT test_record_passfail_check CHECK (((passfail)::text = ANY ((ARRAY['A'::character varying, 'S'::character varying, 'P'::character varying, 'F'::character varying])::text[])))
);


ALTER TABLE public.test_record OWNER TO test1;

--
-- Name: test_record_id_seq; Type: SEQUENCE; Schema: public; Owner: test1
--

CREATE SEQUENCE public.test_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.test_record_id_seq OWNER TO test1;

--
-- Name: test_record_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: test1
--

ALTER SEQUENCE public.test_record_id_seq OWNED BY public.test_record.id;


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
-- Name: test_record id; Type: DEFAULT; Schema: public; Owner: test1
--

ALTER TABLE ONLY public.test_record ALTER COLUMN id SET DEFAULT nextval('public.test_record_id_seq'::regclass);


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
-- Name: test_record test_record_pkey; Type: CONSTRAINT; Schema: public; Owner: test1
--

ALTER TABLE ONLY public.test_record
    ADD CONSTRAINT test_record_pkey PRIMARY KEY (id);


--
-- Name: idx_test_record_calc; Type: INDEX; Schema: public; Owner: test1
--

CREATE INDEX idx_test_record_calc ON public.test_record USING btree (sernum, test_area, record_time);


--
-- Name: idx_test_record_unprocessed; Type: INDEX; Schema: public; Owner: test1
--

CREATE INDEX idx_test_record_unprocessed ON public.test_record USING btree (first_pass_flag) WHERE (first_pass_flag = '-1'::integer);


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

\unrestrict OOigdMfLZhNypb1SLToT7F1JafJtc0vhkjOTSJHaG5ezOrpA8wMH45CC2kUY4sO

