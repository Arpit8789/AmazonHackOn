import { useState } from 'react';
import { Star, ChevronRight, ShieldCheck, AlertTriangle, X, ChevronDown, Truck, MapPin } from 'lucide-react';

const SELLER_RETURN_DATA = [
  { reason: "Product arrived with dents on the side panel", date: "12 May 2025", stars: 2 },
  { reason: "Installation was not done properly by the seller's team", date: "3 Apr 2025", stars: 1 },
  { reason: "Remote control stopped working after 3 days", date: "28 Mar 2025", stars: 2 },
  { reason: "Cooling performance much lower than advertised", date: "15 Feb 2025", stars: 3 },
];

export default function ProductPage1() {
  const [showWarning, setShowWarning] = useState(false);
  const [cartAdded, setCartAdded] = useState(false);
  const [qty, setQty] = useState(1);

  const handleAddToCart = () => {
    setShowWarning(true);
  };

  const confirmAdd = () => {
    setShowWarning(false);
    setCartAdded(true);
    window.dispatchEvent(new Event('addToCart'));
    setTimeout(() => setCartAdded(false), 3000);
  };

  return (
    <div className="bg-white min-h-screen font-sans text-[#0F1111]">
      {/* Breadcrumb */}
      <div className="max-w-[1500px] mx-auto px-5 py-2 text-[12px] text-[#565959]">
        Home & Kitchen › Heating, Cooling & Air Quality › Air Conditioners › <span className="text-[#c45500]">Split Air Conditioners</span>
      </div>

      <div className="max-w-[1500px] mx-auto px-5 flex flex-col lg:flex-row gap-6 pb-10">
        
        {/* LEFT — Product Image */}
        <div className="lg:w-[40%] flex-shrink-0">
          <div className="sticky top-4 border border-[#E7E9EC] rounded-lg p-6 bg-white flex items-center justify-center min-h-[400px]">
            <img src="/product1_ac.jpg" alt="Voltas AC" className="max-h-[380px] max-w-full object-contain" />
          </div>
        </div>

        {/* CENTER — Product Details */}
        <div className="lg:w-[35%] flex-grow">
          <h1 className="text-[24px] leading-[32px] font-normal text-[#0F1111] mb-1">
            Voltas 1.5 Ton 3 Star Inverter Split AC (Copper, 183V CAV, Anti-dust Filter, 2025 Model, White)
          </h1>

          <div className="flex items-center gap-2 mb-2">
            <span className="text-[14px] text-[#007185]">Voltas</span>
            <span className="text-[12px] text-[#565959]">Visit the Voltas Store</span>
          </div>

          {/* Rating */}
          <div className="flex items-center gap-1 mb-3">
            <span className="text-[14px] text-[#007185]">4.1</span>
            <div className="flex">
              {[1,2,3,4].map(i => <Star key={i} size={16} fill="#FFA41C" stroke="#FFA41C"/>)}
              <Star size={16} fill="#E0E0E0" stroke="#E0E0E0"/>
            </div>
            <span className="text-[14px] text-[#007185] ml-1">1,856 ratings</span>
          </div>

          <div className="border-b border-[#E7E9EC] pb-3 mb-3"></div>

          {/* Price */}
          <div className="mb-1">
            <span className="text-[12px] text-[#CC0C39] font-bold">-41%</span>
            <span className="text-[28px] ml-2 font-light">₹36,390</span>
          </div>
          <div className="text-[14px] text-[#565959] mb-4">
            M.R.P.: <span className="line-through">₹61,990</span>
          </div>

          {/* EMI */}
          <div className="bg-[#f7f8f8] border border-[#D5D9D9] rounded p-3 mb-4 text-[13px]">
            EMI starts at ₹1,279. No Cost EMI available. <span className="text-[#007185] cursor-pointer">EMI options ›</span>
          </div>

          {/* About this item */}
          <div className="mb-4">
            <h3 className="text-[16px] font-bold mb-2">About this item</h3>
            <ul className="list-disc pl-5 text-[14px] text-[#333] space-y-1.5 leading-snug">
              <li>1.5 Ton capacity suitable for room size up to 150-180 sq. ft.</li>
              <li>3 Star BEE Rating (2025) for energy savings</li>
              <li>Copper condenser coil for efficient and long-lasting cooling</li>
              <li>Anti-dust filter ensures clean air circulation</li>
              <li>Convertible 4-in-1 cooling for flexibility</li>
              <li>Manufacturer Warranty: 5 years on compressor, 1 year comprehensive</li>
            </ul>
          </div>

          {/* Return & Replacement Policy */}
          <div className="border border-[#E7E9EC] rounded p-4">
            <h3 className="text-[16px] font-bold mb-2">Return, Replacement & Refund Policy</h3>
            <div className="text-[14px] text-[#565959] space-y-1">
              <div className="flex items-center gap-2">
                <ShieldCheck size={16} className="text-[#007185]"/>
                <span>10 days return / replacement</span>
              </div>
              <div className="flex items-center gap-2">
                <Truck size={16} className="text-[#007185]"/>
                <span>Free delivery by Amazon</span>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT — Buy Box */}
        <div className="lg:w-[25%] flex-shrink-0">
          <div className="border border-[#D5D9D9] rounded-lg p-5 sticky top-4">
            <div className="text-[28px] font-light mb-1">₹36,390</div>
            <div className="text-[14px] text-[#565959] mb-3">
              FREE delivery <span className="font-bold text-[#0F1111]">Thursday, 19 June</span>
            </div>
            <div className="flex items-center text-[14px] text-[#007185] mb-4 cursor-pointer">
              <MapPin size={16} className="mr-1"/> Deliver to Chandigarh 140603
            </div>

            <div className="text-[18px] text-[#007600] font-bold mb-4">In stock</div>

            {/* Quantity */}
            <div className="flex items-center gap-2 mb-4">
              <span className="text-[14px]">Quantity:</span>
              <select 
                value={qty} 
                onChange={e => setQty(Number(e.target.value))}
                className="border border-[#D5D9D9] rounded-lg bg-[#F0F2F2] px-2 py-1 text-[13px] shadow-sm"
              >
                {[1,2,3,4,5].map(n => <option key={n} value={n}>{n}</option>)}
              </select>
            </div>

            <button 
              onClick={handleAddToCart}
              className="w-full bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-full py-2 text-[14px] font-medium mb-2 shadow-sm"
            >
              Add to Cart
            </button>
            <button className="w-full bg-[#FFA41C] hover:bg-[#FA8900] border border-[#FF8F00] rounded-full py-2 text-[14px] font-medium mb-4 shadow-sm">
              Buy Now
            </button>

            <div className="text-[12px] text-[#565959] space-y-1">
              <div className="flex justify-between"><span>Sold by</span><span className="text-[#007185]">RetailNet India</span></div>
              <div className="flex justify-between"><span>Fulfilled by</span><span className="text-[#007185]">Amazon</span></div>
            </div>

            {cartAdded && (
              <div className="mt-3 bg-green-50 border border-green-300 text-green-800 text-[13px] p-2 rounded flex items-center">
                <ShieldCheck size={16} className="mr-2"/> Added to Cart!
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ═══ SELLER RETURN WARNING POPUP ═══ */}
      {showWarning && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-lg w-full shadow-2xl overflow-hidden">
            
            {/* Header */}
            <div className="bg-[#FFF8E1] border-b border-[#FFE082] px-5 py-3 flex items-center justify-between">
              <div className="flex items-center">
                <AlertTriangle size={20} className="text-[#F57C00] mr-2" />
                <h3 className="font-bold text-[16px] text-[#0F1111]">Seller Return Feedback</h3>
              </div>
              <button onClick={() => setShowWarning(false)} className="text-gray-500 hover:text-black">
                <X size={18}/>
              </button>
            </div>

            <div className="p-5">
              {/* Return Rate Indicator */}
              <div className="bg-[#FFF3E0] border border-[#FFE0B2] rounded p-3 mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[14px] font-bold text-[#E65100]">This seller has a higher-than-average return rate</span>
                  <span className="text-[20px] font-bold text-[#E65100]">18%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-[#FF9800] h-2 rounded-full" style={{width: '18%'}}></div>
                </div>
                <div className="flex justify-between text-[11px] text-[#565959] mt-1">
                  <span>Average: 4%</span>
                  <span>This seller: 18%</span>
                </div>
              </div>

              {/* Return Reasons */}
              <h4 className="font-bold text-[14px] mb-3 text-[#0F1111]">Recent return reasons from verified buyers:</h4>
              <div className="space-y-3 max-h-[200px] overflow-y-auto mb-4">
                {SELLER_RETURN_DATA.map((item, idx) => (
                  <div key={idx} className="border-b border-[#E7E9EC] pb-2">
                    <div className="flex items-center gap-1 mb-0.5">
                      {Array.from({length: 5}).map((_, i) => (
                        <Star key={i} size={12} fill={i < item.stars ? "#FFA41C" : "#E0E0E0"} stroke={i < item.stars ? "#FFA41C" : "#E0E0E0"}/>
                      ))}
                      <span className="text-[11px] text-[#565959] ml-2">{item.date}</span>
                    </div>
                    <p className="text-[13px] text-[#333]">"{item.reason}"</p>
                  </div>
                ))}
              </div>

              {/* Actions */}
              <div className="flex gap-3">
                <button 
                  onClick={confirmAdd}
                  className="flex-1 bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-full py-2 text-[14px] font-medium shadow-sm"
                >
                  I've reviewed, Continue to Cart
                </button>
                <button 
                  onClick={() => setShowWarning(false)}
                  className="flex-1 bg-white border border-[#D5D9D9] hover:bg-[#F7F8F8] rounded-full py-2 text-[14px] font-medium shadow-sm"
                >
                  Choose a different seller
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
