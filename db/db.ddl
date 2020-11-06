drop table if exists t_documents cascade;

create table t_documents (
  uuid character(36) not null
  , user_uuid character(36) not null
  , name text not null
  , content text not null
  , current_pos integer not null
  , created_at timestamp not null
  , updated_at timestamp not null
  , constraint t_documents_PKC primary key (uuid)
);

drop table if exists t_split_units cascade;

create table t_split_units (
  uuid character(36) not null
  , doc_uuid  character(36) not null
  , index integer not null
  , content text not null
  , constraint t_split_units_PKC primary key (uuid)  
);

drop table if exists t_users cascade;

create table t_users (
  id character(36) not null
  , user_name text not null
  , password text not null
  , constraint t_users_PKC primary key (id)  
);