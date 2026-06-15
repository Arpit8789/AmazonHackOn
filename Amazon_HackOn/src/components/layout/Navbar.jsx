import { Link } from 'react-router-dom';
import { Search, ShoppingCart, MapPin, ChevronDown, Menu } from 'lucide-react';
import { useState, useEffect } from 'react';

const Navbar = () => {
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    const handleAddToCart = () => setCartCount(prev => prev + 1);
    window.addEventListener('addToCart', handleAddToCart);
    return () => window.removeEventListener('addToCart', handleAddToCart);
  }, []);

  return (
    <nav className="bg-[#131921] text-white font-sans flex flex-col">
      {/* ── Top Nav ── */}
      <div className="flex items-center px-2 h-[60px] text-sm">
        
        {/* 1. Logo */}
        <Link to="/" className="flex items-center border border-transparent hover:border-white rounded-sm px-2 h-[50px] shrink-0">
          <img src="/amazon.png" alt="Amazon.in" className="h-[26px] w-auto object-contain" />
          <span className="text-white text-[15px] font-bold ml-0.5 mt-[-8px]">.in</span>
        </Link>

        {/* 2. Address */}
        <div className="hidden sm:flex flex-col border border-transparent hover:border-white rounded-sm px-2 h-[50px] justify-center cursor-pointer shrink-0">
          <div className="text-[#CCCCCC] text-[12px] leading-3 pl-4">Delivering to Chandigarh 140603</div>
          <div className="flex items-center font-bold text-[14px] leading-4 text-white">
            <MapPin size={16} className="mr-1 mt-0.5" />
            Update location
          </div>
        </div>

        {/* 3. Search Bar */}
        <div className="flex flex-1 mx-3 h-[40px] rounded-md overflow-hidden">
          <div className="flex items-center bg-[#E6E6E6] hover:bg-[#D4D4D4] text-[#555] cursor-pointer px-2 border-r border-gray-300 text-[12px] h-full rounded-l-md select-none shrink-0">
            All <ChevronDown size={14} className="ml-0.5 text-gray-500" />
          </div>
          <input 
            type="text" 
            className="flex-1 px-3 py-2 text-black text-[15px] focus:outline-none bg-white"
            placeholder="Search Amazon.in"
          />
          <button className="bg-[#FEBD69] hover:bg-[#F3A847] w-[45px] flex items-center justify-center text-[#333] h-full rounded-r-md focus:outline-none">
            <Search size={22} />
          </button>
        </div>

        {/* Right side items */}
        <div className="flex items-center h-[50px] shrink-0">
          {/* Language */}
          <div className="hidden lg:flex items-center border border-transparent hover:border-white rounded-sm px-2 h-full cursor-pointer text-[14px] gap-1">
            <img src="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg" alt="IN" className="h-4 w-6 object-cover" />
            <span className="font-bold">EN</span>
            <ChevronDown size={12} className="text-gray-400" />
          </div>

          {/* Account & Lists */}
          <div className="hidden lg:flex flex-col border border-transparent hover:border-white rounded-sm px-2 h-full justify-center cursor-pointer">
            <div className="text-[#ccc] text-[12px] leading-3 font-normal">Hello, Sentient</div>
            <div className="font-bold text-[14px] leading-5 flex items-center text-white">
              Account &amp; Lists <ChevronDown size={12} className="ml-0.5 text-gray-400" />
            </div>
          </div>

          {/* Returns & Orders */}
          <Link to="/orders" className="flex flex-col border border-transparent hover:border-white rounded-sm px-2 h-full justify-center">
            <div className="text-[#ccc] text-[12px] leading-3 font-normal">Returns</div>
            <div className="font-bold text-[14px] leading-5 text-white">&amp; Orders</div>
          </Link>

          {/* Cart */}
          <Link to="#" className="flex items-end border border-transparent hover:border-white rounded-sm px-2 h-full cursor-pointer pb-2">
            <div className="relative">
              <ShoppingCart size={32} strokeWidth={2} className="text-white" />
              <span className="absolute -top-1.5 right-[6px] text-[#F08804] font-bold text-[16px] leading-none">{cartCount}</span>
            </div>
            <span className="font-bold text-[14px] text-white ml-1 mb-0.5">Cart</span>
          </Link>
        </div>
      </div>

      {/* ── Bottom Nav ── */}
      <div className="bg-[#232F3E] flex items-center px-2 h-[39px] text-[14px] text-white overflow-x-auto whitespace-nowrap no-scrollbar">
        <div className="flex items-center font-bold border border-transparent hover:border-white rounded-sm px-2 h-[31px] cursor-pointer shrink-0">
          <Menu size={18} className="mr-1" /> All
        </div>
        {[
          'Fresh',
          'MX Player',
          'Sell',
          'Bestsellers',
          "Today's Deals",
          'Mobiles',
        ].map(item => (
          <div key={item} className="border border-transparent hover:border-white rounded-sm px-2 h-[31px] flex items-center cursor-pointer shrink-0">{item}</div>
        ))}
        <div className="border border-transparent hover:border-white rounded-sm px-2 h-[31px] flex items-center cursor-pointer shrink-0">
          Prime <ChevronDown size={12} className="ml-1 text-gray-400" />
        </div>
        {[
          'New Releases',
          'Customer Service',
          'Electronics',
          'Amazon Pay',
          'Fashion',
          'Home & Kitchen',
          'Computers',
          'Toys & Games',
        ].map(item => (
          <div key={item} className="border border-transparent hover:border-white rounded-sm px-2 h-[31px] flex items-center cursor-pointer shrink-0">{item}</div>
        ))}
      </div>
    </nav>
  );
};

export default Navbar;
