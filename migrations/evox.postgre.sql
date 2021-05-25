CREATE SEQUENCE message_id_seq START 1;

CREATE TABLE messages (
    "MessageID" integer NOT NULL DEFAULT nextval('message_id_seq'),
    "Content" character varying(160) NOT NULL,
    "Counter" integer NOT NULL DEFAULT 0,
    CHECK (length("Content")> 0)
);

ALTER TABLE public.messages OWNER TO postgres;

CREATE SEQUENCE account_id_seq START 1;

CREATE TABLE accounts (
    "AccountID" integer NOT NULL DEFAULT nextval('account_id_seq'),
    "Login" character varying(30) NOT NULL,
    "PasswordHash" character varying(128) NOT NULL
);

ALTER TABLE public.accounts OWNER TO postgres;

INSERT INTO messages("Content") VALUES ('Message Content');

INSERT INTO accounts("Login", "PasswordHash") VALUES ('admin', 'f5e86625a8de17e88a0998565af07da067eb1ccad6cb985db76e1bfed4deecb5811cde09281d719ffc6efe6b4a2d3b94f7e823a8c76b987eb995d9602eb0d525');

ALTER TABLE ONLY messages
    ADD CONSTRAINT pk_messages PRIMARY KEY ("MessageID");

ALTER TABLE ONLY accounts
    ADD CONSTRAINT pk_accounts PRIMARY KEY ("AccountID");
