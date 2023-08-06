import OrderForm from "./components/order_form/OrderForm.vue";
import DigitalProducts from "./components/order_form/DigitalProducts.vue";
import DigitalProductsPerson from "./components/order_form/DigitalProductsPerson.vue";
import messages from "./messages.json";

window.router.addRoute({ path: "/app/order/digital_products", component: DigitalProductsPerson, props: true });
window.router.addRoute({ path: "/app/order/digital_products/:key", component: DigitalProducts, props: true });
window.router.addRoute({ path: "/app/order/:formId", component: OrderForm, props: true });

window.i18n.registerLocale(messages);