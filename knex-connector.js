const knex = require('knex')
const config = require('config')
const db_conn = config.get('db_conn')

const connectedKnex = knex({
    client: db_conn.client,
    version: db_conn.version,
    connection: {
        host: db_conn.host,
        user: db_conn.user,
        password: db_conn.password,
        database: db_conn.database,
        port: db_conn.port
    }
})

module.exports = connectedKnex;

