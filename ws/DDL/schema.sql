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
-- Drop table

-- DROP TABLE public.enderecos;

CREATE TABLE public.enderecos (
	end_pk serial NOT NULL,
	end_c_cep bpchar(8) NULL,
	end_c_logradouro varchar(120) NULL,
	end_i_numero int4 NULL,
	end_c_localidade varchar(60) NULL,
	end_c_complemento varchar(120) NULL,
	end_c_bairro varchar(60) NULL,
	CONSTRAINT enderecos_pk PRIMARY KEY (end_pk)
);
CREATE INDEX enderecos_end_pk_idx ON public.enderecos USING btree (end_pk);

-- DROP SEQUENCE public.enderecos_end_pk_seq;

CREATE SEQUENCE public.enderecos_end_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 17
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
	for_fk_perfil int4 NULL,
	for_fk_endereco int4 NULL,
	for_c_formacao varchar(120) NULL,
	for_e_tipo_formacao tipo_formacao NULL,
	for_c_instituicao varchar(60) NULL,
	CONSTRAINT formacoes_pk PRIMARY KEY (for_pk),
	CONSTRAINT fk_for_end FOREIGN KEY (for_fk_endereco) REFERENCES enderecos(end_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE,
	CONSTRAINT fk_for_per FOREIGN KEY (for_fk_perfil) REFERENCES perfis(per_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE
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
	per_fk_endereco int4 NULL,
	per_c_perfil varchar(40) NULL,
	per_d_nascimento date NULL,
	per_c_email varchar(60) NULL,
	per_dt_criado_em_serv timestamp NULL,
	per_c_senha varchar(255) NULL,
	per_c_username varchar(40) NULL,
	CONSTRAINT perfis_pk PRIMARY KEY (per_pk),
	CONSTRAINT fk_per_end FOREIGN KEY (per_fk_endereco) REFERENCES enderecos(end_pk) ON UPDATE CASCADE ON DELETE RESTRICT DEFERRABLE
);

-- DROP SEQUENCE public.perfis_per_pk_seq;

CREATE SEQUENCE public.perfis_per_pk_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 13
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