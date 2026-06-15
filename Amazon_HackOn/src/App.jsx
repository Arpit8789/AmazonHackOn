import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import Orders from './pages/Orders';
import SellerDashboard from './pages/SellerDashboard';
import ProductPage1 from './pages/ProductPage1';
import ProductPage2 from './pages/ProductPage2';
import ProductPage3 from './pages/ProductPage3';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/seller" element={<SellerDashboard />} />
            <Route path="/product/1" element={<ProductPage1 />} />
            <Route path="/product/2" element={<ProductPage2 />} />
            <Route path="/product/3" element={<ProductPage3 />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
