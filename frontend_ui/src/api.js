// import API from './api';
const API_BASE = "http://localhost:5000";


// useEffect(() => {
//   API.get('/products')
//     .then(res => setProducts(res.data))
//     .catch(err => console.error(err));
// }, []);

export async function listProducts() {
  // "http://localhost:5000/product/list_all_products"
  const res = await fetch(`${API_BASE}/product/list_all_products`);
  return res.json();
}
