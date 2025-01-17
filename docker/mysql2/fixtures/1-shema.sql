CREATE DATABASE IF NOT EXISTS metrics_platform;

USE metrics_platform;

CREATE TABLE IF NOT EXISTS codes
(
    id          int auto_increment comment '唯一标识ID' primary key,
    code_type         varchar(100)      null comment '码类型',
    abbrev            varchar(100)      null comment '缩写',
    code_value        varchar(100)      null comment '编码值',
    code_name         varchar(100)      null comment '编码对应描述',
    parent_code_value varchar(100)      null comment '对应父级编码值',
    status            tinyint default 1 null comment '状态',
    is_modifier       tinyint default 0 null comment '是否为修饰词，0否1是(暂不使用)',
    created_at        timestamp         null comment '创建时间',
    updated_at        timestamp         null comment '更新时间',
    created_by        int               null comment '创建人',
    updated_by        int               null comment '更新人',
    description       varchar(100)      null comment '其它描述'
)
 COMMENT '码值管理表' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;


