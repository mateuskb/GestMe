-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION postgres;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP TYPE tipo_formacao;

CREATE TYPE tipo_formacao AS ENUM (
	'Ensino fundamental incompleto',
	'Ensino fundamental completo',
	'Ensino médio incompleto',
	'Ensino médio completo',
	'Superior completo',
	'Pós-graduação',
	'Mestrado',
	'Doutorado',
	'Pós-Doutorado');

-- Drop table

-- DROP TABLE public.categorias;

CREATE TABLE public.categorias (
	cat_pk serial NOT NULL,
	cat_c_categoria varchar(40) NULL,
	CONSTRAINT categorias_pk PRIMARY KEY (cat_pk)
);

-- DROP SEQUENCE public.categorias_cat_pk_seq;

CREATE SEQUENCE public.categorias_cat_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.con_cat;

CREATE TABLE public.con_cat (
	cct_pk serial NOT NULL,
	cct_fk_categoria int4 NULL,
	cct_fk_conteudo int4 NULL,
	CONSTRAINT con_cat_pk PRIMARY KEY (cct_pk),
	CONSTRAINT cct_cat_fk FOREIGN KEY (cct_fk_categoria) REFERENCES categorias(cat_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE,
	CONSTRAINT cct_con_fk FOREIGN KEY (cct_fk_conteudo) REFERENCES conteudos(con_pk) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- DROP SEQUENCE public.con_cat_cct_pk_seq;

CREATE SEQUENCE public.con_cat_cct_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.con_key;

CREATE TABLE public.con_key (
	ck_pk serial NOT NULL,
	ck_fk_conteudo int4 NULL,
	ck_fk_keyword int4 NULL,
	CONSTRAINT con_key_pk PRIMARY KEY (ck_pk),
	CONSTRAINT con_key_fk FOREIGN KEY (ck_fk_conteudo) REFERENCES conteudos(con_pk) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE,
	CONSTRAINT con_key_fk_2 FOREIGN KEY (ck_fk_keyword) REFERENCES keywords(key_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE
);

-- DROP SEQUENCE public.con_key_ck_pk_seq;

CREATE SEQUENCE public.con_key_ck_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.conteudos;

CREATE TABLE public.conteudos (
	con_pk serial NOT NULL,
	con_c_conteudo varchar(40) NULL,
	con_t_descricao text NULL,
	con_dt_cadastrado_em timestamp NULL,
	con_d_criado_em date NULL,
	con_c_image_path varchar(120) NULL,
	con_b_adulto bool NULL DEFAULT false,
	con_c_homepage varchar(255) NULL,
	con_fk_colecao int4 NULL,
	con_c_link varchar(255) NULL,
	con_c_titulo varchar(60) NULL,
	con_fk_tipo int4 NULL,
	CONSTRAINT conteudos_pk PRIMARY KEY (con_pk),
	CONSTRAINT conteudos_fk FOREIGN KEY (con_fk_colecao) REFERENCES colecoes(col_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE,
	CONSTRAINT conteudos_fk_2 FOREIGN KEY (con_fk_tipo) REFERENCES tipo_conteudo(tip_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE
);

-- DROP SEQUENCE public.conteudos_con_pk_seq;

CREATE SEQUENCE public.conteudos_con_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.formacao_for_pk_seq;

CREATE SEQUENCE public.formacao_for_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.formacoes;

CREATE TABLE public.formacoes (
	for_pk serial NOT NULL,
	for_c_formacao varchar NULL,
	CONSTRAINT formacoes_pk PRIMARY KEY (for_pk)
);

-- Drop table

-- DROP TABLE public.historico;

CREATE TABLE public.historico (
	his_pk serial NOT NULL,
	his_fk_perfil int4 NULL,
	his_fk_conteudo int4 NULL,
	his_dt_criado_em timestamp NULL,
	his_i_nota int4 NULL,
	CONSTRAINT historico_pk PRIMARY KEY (his_pk),
	CONSTRAINT fk_his_con FOREIGN KEY (his_fk_conteudo) REFERENCES conteudos(con_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE,
	CONSTRAINT fk_his_per FOREIGN KEY (his_fk_perfil) REFERENCES perfis(per_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE
);

-- DROP SEQUENCE public.historico_his_pk_seq;

CREATE SEQUENCE public.historico_his_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.keywords;

CREATE TABLE public.keywords (
	key_pk serial NOT NULL,
	key_c_keyword varchar(60) NULL,
	CONSTRAINT keywords_pk PRIMARY KEY (key_pk)
);

-- DROP SEQUENCE public.keywords_key_pk_seq;

CREATE SEQUENCE public.keywords_key_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.paises;

CREATE TABLE public.paises (
	pai_pk serial NOT NULL,
	pai_c_pais varchar(60) NULL,
	pai_c_cod varchar(2) NULL,
	CONSTRAINT paises_pk PRIMARY KEY (pai_pk)
);

-- DROP SEQUENCE public.paises_pai_pk_seq;

CREATE SEQUENCE public.paises_pai_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 483
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.perfis;

CREATE TABLE public.perfis (
	per_pk serial NOT NULL,
	per_c_perfil varchar(40) NULL,
	per_d_nascimento date NULL,
	per_c_email varchar(60) NULL,
	per_dt_criado_em_serv timestamp NULL,
	per_c_senha varchar(255) NULL,
	per_c_username varchar(40) NULL,
	per_b_ativo bool NULL DEFAULT false,
	per_fk_pais int4 NULL,
	per_b_email_auth bool NULL DEFAULT false,
	per_fk_formacao int4 NULL,
	CONSTRAINT perfis_pk PRIMARY KEY (per_pk),
	CONSTRAINT perfis_fk FOREIGN KEY (per_fk_pais) REFERENCES paises(pai_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE,
	CONSTRAINT perfis_fk_2 FOREIGN KEY (per_fk_formacao) REFERENCES formacoes(for_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE
);

-- DROP SEQUENCE public.perfis_per_pk_seq;

CREATE SEQUENCE public.perfis_per_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 30
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.ratings;

CREATE TABLE public.ratings (
	rat_pk serial NOT NULL,
	rat_fk_conteudo int4 NULL,
	rat_i_rating int4 NULL,
	CONSTRAINT ratings_pk PRIMARY KEY (rat_pk),
	CONSTRAINT ratings_fk FOREIGN KEY (rat_fk_conteudo) REFERENCES conteudos(con_pk) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE
);

-- DROP SEQUENCE public.ratings_rat_pk_seq;

CREATE SEQUENCE public.ratings_rat_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.colecoes;

CREATE TABLE public.colecoes (
	col_pk serial NOT NULL,
	col_c_colecao varchar(60) NULL,
	col_c_image_path varchar(120) NULL,
	CONSTRAINT colecoes_pk PRIMARY KEY (col_pk)
);
CREATE INDEX colecoes_col_pk_idx ON public.colecoes USING btree (col_pk);

-- Drop table

-- DROP TABLE public.tipo_conteudo;

CREATE TABLE public.tipo_conteudo (
	tip_pk serial NOT NULL,
	tip_c_tipo varchar(40) NULL,
	CONSTRAINT tipo_conteudo_pk PRIMARY KEY (tip_pk)
);
