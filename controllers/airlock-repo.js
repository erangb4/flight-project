const connectedKnex = require("../knex-connector");

function getAll(table_name) {
  return connectedKnex(table_name).select("*");
}

function getByid(table_name, id) {
  return connectedKnex(table_name).select("*").where("id", id).first();
}

function getRaw(query) {
  // run native sql query
  return connectedKnex.raw(query);
}

function addData(table_name, data) {
  return connectedKnex(table_name).insert(data);
}

function updateData(table_name, data, id) {
  return connectedKnex(table_name).where("id", id).update(data);
}

function deleteData(table_name, id) {
  return connectedKnex(table_name).where("id", id).del();
}

module.exports = {
  getAll,
  getByid,
  getRaw,
  addData,
  updateData,
  deleteData,
};
