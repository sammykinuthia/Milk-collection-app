const customerSearch = document.getElementById("customerSearch");
const userItemTemp = document.querySelector("[data-user]");
let username = document.getElementById("username");
let customer = document.getElementById("customer");
let phone = document.getElementById("phone");
let address = document.getElementById("address");
let userError = document.getElementById("user-error");
let milkAmount = document.getElementById("milk-amount");

document
  .getElementById("customerSearchform")
  .addEventListener("submit", (e) => {
    e.preventDefault();
  });

customerSearch.addEventListener("input", (e) => {
  let value = e.target.value;
  fetch(`customers/${value}`)
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        userError.textContent = "user does not exist";
        username.textContent = "";
        phone.textContent = "";
        address.textContent = "";
      } else {
        userError.textContent = "";
        username.textContent = data.username;
        phone.textContent = data.phone;
        address.textContent = data.address;
        customer.setAttribute("value", data.id);
      }
    });
});
// async function getCustomer(usename) {
//   const response = await fetch(`customers/${usename}`);
//   const customers = await response.json();

//   // get value

// }
