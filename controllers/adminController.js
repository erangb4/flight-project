const connectedKnex = require("../knex-connector");
const { logger } = require("../logger");
const { sendMsg } = require("../producer");
const { recieveMsg } = require("../consumer");
const uuid = require("uuid");

const getAllAdmins = async (req, res) => {
  const admins = await connectedKnex("administrators").select("*");
  res.status(200).json({ admins });
};

const getMyData = async (req, res) => {
  const myUser = await connectedKnex("users")
    .select("*")
    .where("username", req.params.user)
    .first();
  const admin = await connectedKnex("administrators")
    .select("*")
    .where("user_id", myUser.id)
    .first();
  res.status(200).json({ admin });
};

const deleteAdmin = async (req, res) => {
  const qResName = `admin ${uuid.v4()}`;
  const myUser = await connectedKnex("users")
    .select("*")
    .where("username", req.params.user)
    .first();
  const admin = await connectedKnex("administrators")
    .select("*")
    .where("user_id", myUser.id)
    .first();
  try {
    reqMsg = {
      action: "deleteAdmin",
      id: admin.id,
      username: req.params.user,
      password: req.body.pwd,
      queue_name: `response ${qResName}`,
    }
    recieveMsg(reqMsg.queue_name, res);
    await sendMsg("admin", reqMsg);
  } catch (e) {
    logger.error(`failed to delete admin. Error: ${e}`);
    res.status(400).send({
      status: "error",
      message: e.message,
    });
  }
};

const updateAdmin = async (req, res) => {
  const qResName = `admin ${uuid.v4()}`;
  try {
    reqMsg = {
      action: "updateAdmin",
      username: req.body.username,
      password: req.body.password,
      id: req.body.id,
      first_name: req.body.firstName,
      last_name: req.body.lastName,
      queue_name: `response ${qResName}`,
    };
    recieveMsg(reqMsg.queue_name, res);
    await sendMsg("admin", reqMsg);
  } catch (e) {
    logger.error(`failed to update admin. Error: ${e}`);
    res.status(400).send({
      status: "error",
      message: e.message,
    });
  }
};

const addAdmin = async (req, res) => {
  try {
    user = {
      username: req.body.username,
      password: req.body.password,
      email: req.body.email,
      user_role: 3, // admin not 3
    };
    const resultUser = await connectedKnex("users").insert(user);
    const newUser = await connectedKnex("users")
      .select("*")
      .where("username", req.body.username)
      .first();
    const resultAdmin = await connectedKnex("administrators").insert({
      first_name: req.body.first_name,
      last_name: req.body.last_name,
      user_id: newUser.id,
    });
    res.status(201).json({
      res: "success",
      url: `${resultAdmin[0]}`,
      result,
    });
  } catch (e) {
    logger.error(`failed to add an admin. Error: ${e}`);
    res.status(400).send({
      status: "error",
      message: e.message,
    });
  }
};

const getAllAirlines = async (req, res) => {
  const airlines = await connectedKnex("airline_companies")
    .select("airline_companies.id", "airline_companies.name", "users.username")
    .orderBy("airline_companies.id", "asc")
    .join("users", function () {
      this.on("airline_companies.user_id", "=", "users.id");
    });
  res.status(200).json({ airlines });
};

const getAirlineById = async (req, res) => {
  const id = req.params.id;
  const airline = await connectedKnex("airline_companies")
    .select("*")
    .where("id", id)
    .first();
  res.status(200).json({ airline });
};

const deleteAirline = async (req, res) => {
  const id = req.params.id;
  try {
    const airline = await connectedKnex("airline_companies")
      .select("*")
      .where("id", id)
      .first();
    const userDel = await connectedKnex("users")
      .where("id", customer.user_id)
      .del();
    const airlineDel = connectedKnex("airline_companies").where("id", id).del();
    res.status(200).json({ num_records_deleted: airlineDel });
  } catch (e) {
    logger.error(`failed to delete an airline. Error: ${e}`);
    res.status(400).send({
      status: "error",
      message: e.message,
    });
  }
};

const addAirline = async (req, res) => {
  try {
    user = {
      username: req.body.username,
      password: req.body.password,
      email: req.body.email,
      user_role: 3,
    };
    const resultUser = await connectedKnex("users").insert(user);
    const newUser = await connectedKnex("users")
      .select("*")
      .where("username", req.body.username)
      .first();
    const resultAirline = await connectedKnex("airline_companies").insert({
      name: req.body.name,
      country_id: req.body.country_id,
      user_id: newUser.id,
    });
    res.status(201).json({
      res: "success",
      url: `/airlines/${resultAirline[0]}`,
      resultAirline,
    });
  } catch (e) {
    logger.error(`failed to add an airline. Error: ${e}`);
    res.status(400).send({
      status: "error",
      message: e.message,
    });
  }
};

const getAllCustomers = async (req, res) => {
  const customers = await connectedKnex("customers").select(
    "customers.id",
    "first_name",
    "last_name",
    "address",
    "phone_number",
    "users.email",
    "credit_card_number",
    "users.username"
  ).join("users", function () {
    this.on("customers.user_id", "=", "users.id");
  });
  res.status(200).json({ customers });
};

const getCustomerById = async (req, res) => {
  const id = req.params.id;
  const customer = await connectedKnex("customers")
    .select("*")
    .where("id", id)
    .first();
  res.status(200).json({ customer });
};

const getAllUsers = async (req, res) => {
  const users = await connectedKnex("users").select("*");
  res.status(200).json({ users });
};

const getUserById = async (req, res) => {
  const id = req.params.id;
  const user = await connectedKnex("users").select("*").where("id", id).first();
  res.status(200).json({ user });
};

const updateUser = async (req, res) => {
  const id = req.params.id;
  try {
    user = req.body;
    const result = await connectedKnex("users").where("id", id).update(user);
    res.status(200).json({
      res: "success",
      url: `/users/${id}`,
      result,
    });
  } catch (e) {
    logger.error(`failed to update user. Error: ${e}`);
    res.status(400).send({
      status: "error",
      message: e.message,
    });
  }
};

module.exports = {
  getAllCustomers,
  getCustomerById,
  getAllAdmins,
  getMyData,
  deleteAdmin,
  updateAdmin,
  addAdmin,
  getAllAirlines,
  getAirlineById,
  deleteAirline,
  addAirline,
  getUserById,
  updateUser,
  getAllUsers,
};
