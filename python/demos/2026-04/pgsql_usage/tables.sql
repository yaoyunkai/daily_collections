DROP TABLE IF EXISTS public.person;

CREATE TABLE IF NOT EXISTS public.person
(
    id integer NOT NULL DEFAULT nextval('person_id_seq'::regclass),
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    gender character varying(1) COLLATE pg_catalog."default" NOT NULL DEFAULT 'N'::character varying,
    birthday date,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT person_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

COMMENT ON COLUMN public.person.gender
    IS '性别字段
N 未知
M 男
W 女';


CREATE SEQUENCE IF NOT EXISTS public.person_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.person_id_seq
    OWNED BY public.person.id;

-- Table: public.post

DROP TABLE IF EXISTS public.post;

CREATE TABLE IF NOT EXISTS public.post
(
    id integer NOT NULL DEFAULT nextval('post_id_seq'::regclass),
    person_id integer,
    title character varying(60) COLLATE pg_catalog."default" NOT NULL,
    content text COLLATE pg_catalog."default" NOT NULL,
    status character varying(1) COLLATE pg_catalog."default" NOT NULL DEFAULT 'S'::character varying,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT post_pkey PRIMARY KEY (id),
    CONSTRAINT fk_post_person FOREIGN KEY (person_id)
        REFERENCES public.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

COMMENT ON TABLE public.post
    IS '发表的文章';

COMMENT ON COLUMN public.post.title
    IS '文章标题';

COMMENT ON COLUMN public.post.status
    IS '文章的状态
S 草稿状态
T 待审核
D 审核完成';

CREATE SEQUENCE IF NOT EXISTS public.post_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.post_id_seq
    OWNED BY public.post.id;