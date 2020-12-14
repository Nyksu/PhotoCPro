CREATE TABLE countries (
 id SERIAL NOT NULL ,
 name VARCHAR(50) ,
 short CHAR(4) ,
PRIMARY KEY(id));

CREATE TABLE settings (
 idsetting SERIAL NOT NULL ,
PRIMARY KEY(idsetting));

CREATE TABLE currencies (
 id SERIAL NOT NULL ,
 name VARCHAR(50) NOT NULL ,
 short CHAR(3) NOT NULL ,
PRIMARY KEY(id));

CREATE TABLE lexicons (
 id SERIAL NOT NULL ,
 code VARCHAR(50) NOT NULL ,
 category INTEGER DEFAULT 0 ,
 comment_phrase VARCHAR(250) ,
PRIMARY KEY(id) );

CREATE INDEX lexicon_code_idx ON lexicons (code);
CREATE INDEX lexicons_category_idx ON lexicons (category);

CREATE TABLE languages (
 id SERIAL NOT NULL ,
 name VARCHAR(50) NOT NULL ,
 name_dialect VARCHAR(50) ,
 short CHAR(4) ,
PRIMARY KEY(id));

CREATE TABLE versions (
 base_ver VARCHAR(20) NOT NULL ,
 server_ver VARCHAR(20) ,
 client_ver VARCHAR(20) ,
 release VARCHAR(20) );

CREATE TABLE users (
 id SERIAL NOT NULL ,
 first_name VARCHAR(50) NOT NULL ,
 last_name VARCHAR(50) NOT NULL ,
 nick_name VARCHAR(20) NOT NULL ,
 psw VARCHAR(100) NOT NULL ,
 salt VARCHAR(200) ,
 avatar VARCHAR(200) ,
 email VARCHAR(50) NOT NULL ,
 phone VARCHAR(20) ,
 user_type INTEGER NOT NULL ,
 email_state INTEGER NOT NULL ,
 email_code VARCHAR(50) ,
 biography TEXT ,
 awards TEXT ,
 date_create DATE NOT NULL ,
 row_state INTEGER NOT NULL ,
PRIMARY KEY(id) );

CREATE INDEX users_usertype_idx ON users (user_type);
CREATE UNIQUE INDEX users_nick_name_idx ON users (nick_name);
CREATE UNIQUE INDEX users_email_idx ON users (email);
CREATE INDEX users_email_state_idx ON users (email_state);

CREATE TABLE award_types (
 id SERIAL NOT NULL ,
 name VARCHAR(20) NOT NULL ,
 img VARCHAR(100) ,
PRIMARY KEY(id));

CREATE TABLE organizers (
 id SERIAL NOT NULL ,
 language_id INTEGER NOT NULL ,
 name VARCHAR(255) NOT NULL ,
 email_sys VARCHAR(50) NOT NULL ,
 email_pub VARCHAR(50) NOT NULL ,
 address_line1 VARCHAR(100) ,
 address_line2 VARCHAR(100) ,
 www VARCHAR(50) ,
 phone VARCHAR(20) ,
 phone_tech VARCHAR(20) ,
 officer VARCHAR(100) ,
 logo VARCHAR(100) ,
 virtual INTEGER DEFAULT 0 NOT NULL ,
 smtp VARCHAR(50) ,
 smtp_psw VARCHAR(50) ,
 smtp_user VARCHAR(50) ,
 smtp_use_pub INTEGER DEFAULT 0 NOT NULL ,
 date_create DATE NOT NULL ,
 row_state INTEGER DEFAULT 0 NOT NULL ,
 date_status DATE NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(language_id)
 REFERENCES languages(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE UNIQUE INDEX organizer_name_idx ON organizers (name);
CREATE INDEX organizer_status_idx ON organizers (row_state);
CREATE INDEX organizer_virtual_idx ON organizers (virtual);
CREATE INDEX organizer_FK_language_idx ON organizers (language_id);


CREATE TABLE admin_menus (
 id SERIAL NOT NULL ,
 lexicon_id INTEGER NOT NULL ,
 position INTEGER DEFAULT 0 NOT NULL ,
 parent_id INTEGER DEFAULT 0 NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(lexicon_id)
 REFERENCES lexicons(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX admin_menus_FK_lexicon_idx ON admin_menus (lexicon_id);


CREATE TABLE spr_salone_types (
 id SERIAL NOT NULL ,
 lexicon_id INTEGER NOT NULL ,
 name VARCHAR(50) NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(lexicon_id)
 REFERENCES lexicons(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX spr_salone_types_FK_lexicon_idx ON spr_salone_types (lexicon_id);


CREATE TABLE salones (
 id SERIAL NOT NULL ,
 spr_salone_type_id INTEGER NOT NULL ,
 organizer_id INTEGER NOT NULL ,
 name VARCHAR(100) NOT NULL ,
 regular INTEGER NOT NULL ,
 private INTEGER NOT NULL ,
 domain VARCHAR(50) NOT NULL ,
 design_code VARCHAR(20) NOT NULL ,
 row_state INTEGER NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(organizer_id)
 REFERENCES organizers(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(spr_salone_type_id)
 REFERENCES spr_salone_types(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX salone_FK_organizer_idx ON salones (organizer_id);
CREATE INDEX salone_FK_spr_salone_type_idx ON salones (spr_salone_type_id);
CREATE INDEX salone_regular_idx ON salones (regular);
CREATE INDEX salone_row_state_idx ON salones (row_state);
CREATE INDEX salone_private_idx ON salones (private);


CREATE TABLE salone_abouts (
 id SERIAL NOT NULL ,
 language_id INTEGER NOT NULL ,
 salone_id INTEGER NOT NULL ,
 name VARCHAR(200) ,
 content TEXT ,
PRIMARY KEY(id) ,
 FOREIGN KEY(salone_id)
 REFERENCES salones(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(language_id)
 REFERENCES languages(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX salone_about_FK_salone_idx ON salone_abouts (salone_id);
CREATE INDEX salone_about_FK_language_idx ON salone_abouts (language_id);


CREATE TABLE admins (
 organizer_id INTEGER NOT NULL ,
 user_id INTEGER NOT NULL ,
 adm_type INTEGER NOT NULL ,
 FOREIGN KEY(user_id)
 REFERENCES users(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(organizer_id)
 REFERENCES organizers(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX admins_FK_user_idx ON admins (user_id);
CREATE INDEX admins_FK_organizer_idx ON admins (organizer_id);


CREATE TABLE phrases (
 id SERIAL NOT NULL ,
 lexicon_id INTEGER NOT NULL ,
 language_id INTEGER NOT NULL ,
 name VARCHAR(250) ,
PRIMARY KEY(id) ,
 FOREIGN KEY(language_id)
 REFERENCES languages(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(lexicon_id)
 REFERENCES lexicons(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX phrases_FK_language_idx ON phrases (language_id);
CREATE INDEX phrases_FK_lexicon_idx ON phrases (lexicon_id);
CREATE UNIQUE INDEX phrases_language_lexicon_idx ON phrases (lexicon_id, language_id);


CREATE TABLE lockalposts (
 id SERIAL NOT NULL ,
 user_id INTEGER NOT NULL ,
 recipient_id INTEGER NOT NULL ,
 about VARCHAR(50) NOT NULL ,
 content TEXT NOT NULL ,
 date_create DATE NOT NULL ,
 date_read DATE ,
 rating INTEGER DEFAULT 0 NOT NULL ,
 row_state INTEGER DEFAULT 0 NOT NULL ,
 need_email INTEGER DEFAULT 0 NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(user_id)
 REFERENCES users(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(recipient_id)
 REFERENCES users(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX lockalpost_FK_user_idx ON lockalposts (user_id);
CREATE INDEX lockalpost_FK_users2_idx ON lockalposts (recipient_id);


CREATE TABLE customers (
 country_id INTEGER NOT NULL ,
 user_id INTEGER NOT NULL ,
 salone_id INTEGER NOT NULL ,
 address VARCHAR(100) NOT NULL ,
 post_index CHAR(6) ,
 birthday DATE ,
 FOREIGN KEY(user_id)
 REFERENCES users(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(salone_id)
 REFERENCES salones(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE,
 FOREIGN KEY(country_id)
 REFERENCES countries(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX customer_FK_user_idx ON customers (user_id);
CREATE INDEX customer_FK_salone_idx ON customers (salone_id);
CREATE INDEX customer_FK_country_idx ON customers (country_id);


CREATE TABLE contests (
 id SERIAL NOT NULL ,
 salone_id INTEGER NOT NULL ,
 subname VARCHAR(100) NOT NULL ,
 years CHAR(4) ,
 date_start DATE NOT NULL ,
 date_stop DATE NOT NULL ,
 date_juri_end DATE NOT NULL ,
 date_rate_show DATE NOT NULL ,
 show_type INTEGER NOT NULL ,
 show_rate_state INTEGER NOT NULL ,
 democraty INTEGER NOT NULL ,
 pay_type INTEGER ,
 section_count INTEGER ,
 maxrate INTEGER DEFAULT 10 ,
 maxsize INTEGER DEFAULT 0 ,
 max_weight INTEGER DEFAULT 0 ,
PRIMARY KEY(id) ,
 FOREIGN KEY(salone_id)
 REFERENCES salones(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX contest_FK_salone_idx ON contests (salone_id);


CREATE TABLE registration_contests (
 id SERIAL NOT NULL ,
 user_id INTEGER NOT NULL ,
 contest_id INTEGER NOT NULL ,
 date_reg DATE NOT NULL ,
 section_count INTEGER NOT NULL ,
 reg_state INTEGER NOT NULL ,
 rejection_reason VARCHAR(100) ,
 payment INTEGER DEFAULT 0 NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(user_id)
 REFERENCES users(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(contest_id)
 REFERENCES contests(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX registration_contest_FK_user_idx ON registration_contests (user_id);
CREATE INDEX registration_contest_FK_contest_idx ON registration_contests (contest_id);
CREATE UNIQUE INDEX registration_contests_user_contest_idx ON registration_contests (user_id, contest_id);


CREATE TABLE contest_menus (
 id SERIAL NOT NULL ,
 lexicon_id INTEGER NOT NULL ,
 contest_id INTEGER NOT NULL ,
 position INTEGER DEFAULT 0 NOT NULL ,
 parent_id INTEGER DEFAULT 0 NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(contest_id)
 REFERENCES contests(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(lexicon_id)
 REFERENCES lexicons(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX contest_menus_FK_contest_idx ON contest_menus (contest_id);
CREATE INDEX contest_menus_FK_lexicon_idx ON contest_menus (lexicon_id);


CREATE TABLE contest_abouts (
 id SERIAL NOT NULL ,
 language_id INTEGER NOT NULL ,
 contest_id INTEGER NOT NULL ,
 name VARCHAR(100) ,
 thesis TEXT ,
 rules TEXT ,
PRIMARY KEY(id) ,
 FOREIGN KEY(contest_id)
 REFERENCES contests(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(language_id)
 REFERENCES languages(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX contest_about_FK_contest_idx ON contest_abouts (contest_id);
CREATE INDEX contest_about_FK_language_idx ON contest_abouts (language_id);


CREATE TABLE awards_stacks (
 id SERIAL NOT NULL ,
 contest_id INTEGER NOT NULL ,
 award_type_id INTEGER NOT NULL ,
 position INTEGER DEFAULT 10 NOT NULL ,
 count_awards INTEGER DEFAULT 1 NOT NULL ,
 issued INTEGER DEFAULT 0 NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(award_type_id)
 REFERENCES award_types(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE,
 FOREIGN KEY(contest_id)
 REFERENCES contests(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX awards_stack_FK_award_type_idx ON awards_stacks (award_type_id);
CREATE INDEX awards_stack_FK_contest_idx ON awards_stacks (contest_id);


CREATE TABLE invoices (
 id SERIAL NOT NULL ,
 registration_salone_id INTEGER NOT NULL ,
 currency_id INTEGER NOT NULL ,
 date_create DATE NOT NULL ,
 date_pay DATE ,
 amount FLOAT NOT NULL ,
 pay_value FLOAT DEFAULT 0 NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(currency_id)
 REFERENCES currencies(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE,
 FOREIGN KEY(registration_salone_id)
 REFERENCES registration_contests(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX invoice_FK_currency_idx ON invoices (currency_id);
CREATE INDEX invoice_FK_registration_salone_idx ON invoices (registration_salone_id);


CREATE TABLE juries (
 id SERIAL NOT NULL ,
 contest_id INTEGER NOT NULL ,
 user_id INTEGER NOT NULL ,
 rank VARCHAR(100) ,
PRIMARY KEY(id) ,
 FOREIGN KEY(user_id)
 REFERENCES users(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(contest_id)
 REFERENCES contests(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX jury_FK_user_idx ON juries (user_id);
CREATE INDEX jury_FK_contest_idx ON juries (contest_id);


CREATE TABLE partners (
 id SERIAL NOT NULL ,
 contest_id INTEGER NOT NULL ,
 name VARCHAR(200) NOT NULL ,
 banner VARCHAR(200) ,
 linkaddress VARCHAR(200) ,
 banner_small VARCHAR(200) ,
 type_2 INTEGER NOT NULL ,
 banner_type INTEGER ,
 srow_state INTEGER ,
PRIMARY KEY(id) ,
 FOREIGN KEY(contest_id)
 REFERENCES contests(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX parners_FK_contest_idx ON partners (contest_id);


CREATE TABLE sections (
 id SERIAL NOT NULL ,
 contest_id INTEGER NOT NULL ,
 max_count_img INTEGER NOT NULL ,
 name VARCHAR(100) NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(contest_id)
 REFERENCES contests(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX sections_FK_contest_idx ON sections (contest_id);


CREATE TABLE publications (
 id SERIAL NOT NULL ,
 contest_menu_id INTEGER NOT NULL ,
 date_create DATE NOT NULL ,
 date_show DATE ,
 visible INTEGER NOT NULL ,
 pubtype INTEGER DEFAULT 0 NOT NULL ,
 archive INTEGER DEFAULT 0 NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(contest_menu_id)
 REFERENCES contest_menus(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX publications_FK_contests_menu_idx ON publications (contest_menu_id);


CREATE TABLE publictxts (
 id SERIAL NOT NULL ,
 language_id INTEGER NOT NULL ,
 publication_id INTEGER NOT NULL ,
 name VARCHAR(100) NOT NULL ,
 content TEXT NOT NULL ,
 digest VARCHAR(250) ,
PRIMARY KEY(id) ,
 FOREIGN KEY(publication_id)
 REFERENCES publications(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(language_id)
 REFERENCES languages(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX publictxt_FK_publication_idx ON publictxts (publication_id);
CREATE INDEX publictxt_FK_language_idx ON publictxts (language_id);


CREATE TABLE photoworks (
 id SERIAL NOT NULL ,
 registration_contest_id INTEGER NOT NULL ,
 section_id INTEGER NOT NULL ,
 name VARCHAR(100) NOT NULL ,
 filename VARCHAR(200) NOT NULL ,
 moder INTEGER DEFAULT 0 NOT NULL ,
 reason_moderation VARCHAR(100) ,
 date_add DATE NOT NULL ,
 average FLOAT DEFAULT 0 ,
 median FLOAT DEFAULT 0 ,
 demos_rate INTEGER DEFAULT 0 ,
 year_shot CHAR(4) ,
 locate_shot VARCHAR(200) ,
PRIMARY KEY(id) ,
 FOREIGN KEY(registration_contest_id)
 REFERENCES registration_contests(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(section_id)
 REFERENCES sections(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX photowork_FK_registration_contest_idx ON photoworks (registration_contest_id);
CREATE INDEX photowork_FK_section_idx ON photoworks (section_id);

CREATE TABLE rates (
 id SERIAL NOT NULL ,
 photowork_id INTEGER NOT NULL ,
 jury_id INTEGER NOT NULL ,
 rate_value FLOAT NOT NULL ,
 date_rate DATE NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(jury_id)
 REFERENCES juries(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(photowork_id)
 REFERENCES photoworks(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX rates_FK_jury_idx ON rates (jury_id);
CREATE INDEX rates_FK_photowork_idx ON rates (photowork_id);

CREATE TABLE awards (
 id SERIAL NOT NULL ,
 photowork_id INTEGER NOT NULL ,
 awards_stack_id INTEGER NOT NULL ,
PRIMARY KEY(id) ,
 FOREIGN KEY(awards_stack_id)
 REFERENCES awards_stacks(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE,
 FOREIGN KEY(photowork_id)
 REFERENCES photoworks(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE);

CREATE INDEX awards_FK_awards_stack_idx ON awards (awards_stack_id);
CREATE INDEX awards_FK_photowork_idx ON awards (photowork_id);
CREATE UNIQUE INDEX awards_stack_photowork_idx ON awards (photowork_id, awards_stack_id);

CREATE TABLE section_names (
 id SERIAL NOT NULL,
 language_id INTEGER NOT NULL,
 section_id INTEGER NOT NULL,
 name VARCHAR(100) NOT NULL,
PRIMARY KEY(id),
 FOREIGN KEY(section_id)
 REFERENCES sections(id)
 ON DELETE CASCADE
 ON UPDATE CASCADE,
 FOREIGN KEY(language_id)
 REFERENCES languages(id)
 ON DELETE RESTRICT
 ON UPDATE CASCADE);

CREATE INDEX section_names_FK_sections_idx ON section_names (section_id);
CREATE INDEX section_names_FK_languages_idx ON section_names (language_id);

create view rates_jury as
  select x_r.*, x_j.user_id from rates x_r, juries x_j 
  where  
    x_r.jury_id = x_j.id;

insert into versions(base_ver, server_ver, client_ver, release) values ('0.0.8','','','');
  