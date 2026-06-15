import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ChevronLeft, ChevronRight, Star, Leaf, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

const HERO_SLIDES = [
  { id: 1, image: '/hero_slide1_right.jpg', alt: 'Hero Banner 1' },
  { id: 2, image: '/hero_slide2_right.jpg', alt: 'Hero Banner 2' },
  { id: 3, image: '/hero_slide3_right.jpg', alt: 'Hero Banner 3' },
  { id: 4, image: '/hero_slide4_right.jpg', alt: 'Hero Banner 4' },
  { id: 5, image: '/hero_slide5_right.jpg', alt: 'Hero Banner 5' },
  { id: 6, image: '/hero_slide6_right.png', alt: 'Second Life Commerce' },
];

export default function Home() {
  const [currentSlide, setCurrentSlide] = useState(0);

  const { data: products } = useQuery({
    queryKey: ['demo-products'],
    queryFn: async () => {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
      const res = await fetch(`${apiUrl}/demo/products`);
      const json = await res.json();
      return json.data;
    }
  });

  const secondLifeProducts = products?.filter(p => p.is_second_life) || [];
  const regularProducts = products?.filter(p => !p.is_second_life && !['P004', 'P005'].includes(p.product_id)) || [];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide(s => (s + 1) % HERO_SLIDES.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="bg-[#E3E6E6] min-h-screen relative pb-10 font-sans">

      {/* ── HERO CAROUSEL ────────────────────────────────── */}
      <div className="relative w-full h-[600px] overflow-hidden">
        {HERO_SLIDES.map((slide, i) => (
          <div
            key={slide.id}
            className={`absolute inset-0 transition-opacity duration-700
                        ${i === currentSlide ? 'opacity-100 z-10' : 'opacity-0 z-0'}`}
          >
            {/* Single full-width image per slide */}
            <img
              src={slide.image}
              alt={slide.alt}
              className="w-full h-full object-cover object-top"
            />
            {/* Bottom gradient fade into background */}
            <div className="absolute inset-x-0 bottom-0 h-[250px] bg-gradient-to-t from-[#E3E6E6] to-transparent z-10" />
          </div>
        ))}

        {/* Carousel controls */}
        <button
          onClick={() => setCurrentSlide(s => s === 0 ? HERO_SLIDES.length - 1 : s - 1)}
          className="absolute top-1/3 left-0 z-20 text-white hover:bg-white/10 px-2 py-10 rounded-r-sm transition-colors"
        >
          <ChevronLeft size={48} strokeWidth={1} />
        </button>
        <button
          onClick={() => setCurrentSlide(s => (s + 1) % HERO_SLIDES.length)}
          className="absolute top-1/3 right-0 z-20 text-white hover:bg-white/10 px-2 py-10 rounded-l-sm transition-colors"
        >
          <ChevronRight size={48} strokeWidth={1} />
        </button>
      </div>

      {/* ── QUAD CARDS — overlapping bottom of hero ────── */}
      <div className="max-w-[1500px] mx-auto px-5 -mt-[300px] relative z-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">

          {/* Card 1 */}
          <div 
            onClick={() => document.getElementById('products-you-may-like')?.scrollIntoView({ behavior: 'smooth' })}
            className="bg-white p-5 flex flex-col h-[420px] shadow-md relative z-20 rounded-xl overflow-hidden cursor-pointer hover:shadow-lg transition-shadow"
          >
            <h2 className="text-[21px] font-bold mb-4 text-[#0F1111] leading-tight">Appliances for your home | Up to 55% off</h2>
            <div className="grid grid-cols-2 gap-4 flex-1 pointer-events-none">
              <div className="flex flex-col"><img src="/card1_img1.png" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Air conditioners</span></div>
              <div className="flex flex-col"><img src="/card1_img2.png" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Refrigerators</span></div>
              <div className="flex flex-col"><img src="/card1_img3.png" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Microwaves</span></div>
              <div className="flex flex-col"><img src="/card1_img4.png" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Washing machines</span></div>
            </div>
            <span className="text-[#007185] text-[13px] hover:text-[#C45500] hover:underline mt-4">See more</span>
          </div>

          {/* Card 2 */}
          <div 
            onClick={() => document.getElementById('products-you-may-like')?.scrollIntoView({ behavior: 'smooth' })}
            className="bg-white p-5 flex flex-col h-[420px] shadow-md relative z-20 rounded-xl overflow-hidden cursor-pointer hover:shadow-lg transition-shadow"
          >
            <h2 className="text-[21px] font-bold mb-4 text-[#0F1111] leading-tight">Revamp your home in style</h2>
            <div className="grid grid-cols-2 gap-4 flex-1 pointer-events-none">
              <div className="flex flex-col"><img src="/card2_img1.jpeg" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Cushion covers, bedsheets</span></div>
              <div className="flex flex-col"><img src="/card2_img2.jpeg" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Figurines, vases & more</span></div>
              <div className="flex flex-col"><img src="/card2_img3.jpeg" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Home storage</span></div>
              <div className="flex flex-col"><img src="/card2_img4.jpeg" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Lighting solutions</span></div>
            </div>
            <span className="text-[#007185] text-[13px] hover:text-[#C45500] hover:underline mt-4">Explore all</span>
          </div>

          {/* Card 3 */}
          <div 
            onClick={() => document.getElementById('products-you-may-like')?.scrollIntoView({ behavior: 'smooth' })}
            className="bg-white p-5 flex flex-col h-[420px] shadow-md relative z-20 rounded-xl overflow-hidden cursor-pointer hover:shadow-lg transition-shadow"
          >
            <h2 className="text-[21px] font-bold mb-4 text-[#0F1111] leading-tight">Starting ₹49 | Deals on home essentials</h2>
            <div className="grid grid-cols-2 gap-4 flex-1 pointer-events-none">
              <div className="flex flex-col"><img src="/card3_img1.jpeg" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Cleaning supplies</span></div>
              <div className="flex flex-col"><img src="/card3_img2.jpeg" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Bathroom accessories</span></div>
              <div className="flex flex-col"><img src="/card3_img3.jpeg" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Home tools</span></div>
              <div className="flex flex-col"><img src="/card3_img4.jpeg" className="h-[105px] w-full object-cover mb-1 rounded-md" /><span className="text-[12px] text-[#0F1111]">Wallpapers</span></div>
            </div>
            <span className="text-[#007185] text-[13px] hover:text-[#C45500] hover:underline mt-4">Explore all</span>
          </div>

          {/* Card 4 - Second Life Dedicated Card */}
          <div 
            onClick={() => document.getElementById('second-life')?.scrollIntoView({ behavior: 'smooth' })}
            className="bg-white p-5 flex flex-col h-[420px] shadow-md relative z-20 border-2 border-green-600 rounded-xl overflow-hidden cursor-pointer hover:shadow-lg transition-shadow"
          >
            <h2 className="text-[21px] font-bold mb-4 text-[#0F1111] leading-tight pointer-events-none">Pre-Owned & Sustainable (Second Life)</h2>
            <div className="flex-1 overflow-hidden rounded-md pointer-events-none">
              <img src="/secondlife.png" alt="Second Life" className="h-[250px] w-full object-cover" />
            </div>
            <span className="text-[#007185] text-[13px] hover:text-[#C45500] hover:underline mt-4">Discover verified pre-owned items</span>
          </div>

        </div>

        {/* ── PRODUCTS YOU MAY LIKE (AI Return Prevention Demos) ───────────────────────── */}
        <div id="products-you-may-like" className="mt-6 bg-white p-5 shadow-md rounded-xl scroll-mt-20">
          <div className="flex items-center mb-4">
            <h2 className="text-[21px] font-bold text-[#0F1111]">Products you may like</h2>
            <span className="ml-4 text-[14px] text-[#007185] hover:underline hover:text-[#C45500] cursor-pointer">Explore featured items</span>
          </div>

          <div className="flex gap-4 overflow-x-auto pb-4 pt-2 no-scrollbar">
            {regularProducts.map(product => (
              <Link key={product.product_id} to={`/product/${product.product_id.replace('P00', '')}`}>
                <div className="min-w-[200px] max-w-[200px] flex flex-col cursor-pointer group">
                  <div className="h-[200px] w-full bg-[#f7f7f7] flex items-center justify-center mb-2 relative overflow-hidden">
                    <img src={product.image_url} className="max-h-[180px] max-w-[180px] object-contain mix-blend-multiply group-hover:scale-105 transition-transform" />
                  </div>
                  <div className="text-[21px] font-normal text-[#0F1111] mb-0.5 leading-none">
                    <span className="text-[13px] align-top mr-0.5">₹</span>{product.original_price}
                  </div>
                  <div className="text-[14px] text-[#0F1111] line-clamp-2 hover:text-[#C45500]">
                    {product.name}
                  </div>
                  <div className="flex items-center mt-1">
                    {[1, 2, 3, 4].map(i => <Star key={i} size={14} fill="#FFA41C" stroke="#FFA41C" />)}
                    <Star size={14} fill="#E0E0E0" stroke="#E0E0E0" />
                    <span className="text-[12px] text-[#007185] ml-1">1,234</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* ── SECOND LIFE SCROLLER ROW ───────────────────────── */}
        {secondLifeProducts.length > 0 && (
          <div id="second-life" className="mt-6 bg-white p-5 shadow-md border-2 border-[#146e29] rounded-xl scroll-mt-20">
            <div className="flex items-center mb-4">
              <h2 className="text-[21px] font-bold text-[#0F1111]">Amazon Second Life</h2>
              <span className="ml-4 text-[14px] text-[#007185] hover:underline hover:text-[#C45500] cursor-pointer">Shop certified pre-owned items with warranty</span>
            </div>

            <div className="flex gap-4 overflow-x-auto pb-4 pt-2 no-scrollbar">
              {secondLifeProducts.map(product => (
                <Link key={product.product_id} to="/product/1">
                  <div className="min-w-[200px] max-w-[200px] flex flex-col cursor-pointer group">
                    <div className="h-[200px] w-full bg-[#f7f7f7] flex items-center justify-center mb-2 relative overflow-hidden">
                      <img src={product.image_url} className="max-h-[180px] max-w-[180px] object-contain mix-blend-multiply group-hover:scale-105 transition-transform" />
                      <div className="absolute top-0 left-0 bg-[#0F1111] text-white text-[10px] font-bold px-2 py-0.5 rounded-br-lg shadow-sm">
                        <ShieldCheck size={10} className="inline mr-1" /> 6 Months Warranty
                      </div>
                    </div>

                    {/* Instant Discount */}
                    <div className="flex items-center text-xs mb-1">
                      <span className="bg-[#CC0C39] text-white px-1.5 py-0.5 font-bold mr-2 rounded-sm text-[11px]">
                        -{Math.round((1 - product.second_life_price / product.original_price) * 100)}%
                      </span>
                      <span className="text-[#CC0C39] font-bold text-[12px]">Instant Discount</span>
                    </div>

                    <div className="text-[21px] font-normal text-[#0F1111] mb-0.5 leading-none">
                      <span className="text-[13px] align-top mr-0.5">₹</span>{product.second_life_price}
                    </div>

                    <div className="text-[12px] text-gray-500 mb-1">
                      M.R.P.: <span className="line-through">₹{product.original_price}</span>
                    </div>

                    <div className="text-[14px] text-[#0F1111] line-clamp-2 hover:text-[#C45500]">
                      {product.name}
                    </div>

                    {/* Grade indicator removed per user request */}

                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        window.dispatchEvent(new Event('addToCart'));
                      }}
                      className="mt-2 bg-[#FFD814] hover:bg-[#F7CA00] text-[#0F1111] text-[12px] py-1.5 px-3 rounded-full font-medium w-full shadow-sm z-10 relative"
                    >
                      Add to Cart
                    </button>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
