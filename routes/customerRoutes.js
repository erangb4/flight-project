const { Router } = require("express");
const router = Router();
const {
  deleteCustomer,
  updateCustomer,
  getMyTickets,
  getMyData,
  addTicket,
  removeTicket,
} = require("../controllers/customerController");

router
  .route("/tickets/:user")
  .get(getMyTickets)
  .post(addTicket)
  .delete(removeTicket);
router
  .route("/:user")
  .delete(deleteCustomer)
  .put(updateCustomer)
  .get(getMyData);

module.exports = router;
