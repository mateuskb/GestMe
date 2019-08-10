-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION postgres;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP TYPE _tipo_formacao;

CREATE TYPE _tipo_formacao (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 4,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tipo_formacao,
	DELIMITER = ',');

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

-- DROP TABLE public.conteudos;

CREATE TABLE public.conteudos (
	con_pk serial NOT NULL,
	con_c_conteudo varchar(40) NULL,
	con_t_descricao text NULL,
	con_dt_cadastrado_em timestamp NULL,
	con_d_criado_em date NULL,
	con_c_path varchar(120) NULL,
	CONSTRAINT conteudos_pk PRIMARY KEY (con_pk)
);

-- DROP SEQUENCE public.conteudos_con_pk_seq;

CREATE SEQUENCE public.conteudos_con_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.enderecos_end_pk_seq;

CREATE SEQUENCE public.enderecos_end_pk_seq
	NO MINVALUE
	NO MAXVALUE
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
	START 15
	CACHE 1
	NO CYCLE;
-- Drop table

-- DROP TABLE public.relacionamento_categorias;

CREATE TABLE public.relacionamento_categorias (
	rel_pk serial NOT NULL,
	rel_fk_categorias_1 int4 NULL,
	rel_fk_categorias_2 int4 NULL,
	CONSTRAINT relacionamento_categorias_pk PRIMARY KEY (rel_pk),
	CONSTRAINT fk_rel_cat_1 FOREIGN KEY (rel_fk_categorias_1) REFERENCES categorias(cat_pk) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE,
	CONSTRAINT fk_rel_cat_2 FOREIGN KEY (rel_fk_categorias_2) REFERENCES categorias(cat_pk) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE
);

-- DROP SEQUENCE public.relacionamento_categorias_rel_pk_seq;

CREATE SEQUENCE public.relacionamento_categorias_rel_pk_seq
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
