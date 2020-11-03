drop table if exists t_documents cascade;

create table t_documents (
  uuid character(36) not null
  , content text not null
  , split_uuid character(36) not null
  , current_pos integer not null
  , created_at timestamp not null
  , updated_at timestamp not null
  , constraint t_documents_PKC primary key (uuid)
);

drop table if exists t_split_units cascade;

create table t_split_units (
  uuid character(36) not null
  , index integer not null
  , content text not null
  , constraint t_split_units_PKC primary key (uuid)  
);