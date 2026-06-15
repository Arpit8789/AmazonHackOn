import { useState } from 'react';
import { Star, ShieldCheck, AlertTriangle, X, Truck, MapPin, Ruler } from 'lucide-react';

const SIZE_CHART = [
  { uk: 6, cm: 24.5 }, { uk: 7, cm: 25.5 }, { uk: 8, cm: 26.5 },
  { uk: 9, cm: 27.5 }, { uk: 10, cm: 28.5 },
];

export default function ProductPage2() {
  const [selectedSize, setSelectedSize] = useState(null);
  const [showSizeWarning, setShowSizeWarning] = useState(false);
  const [cartAdded, setCartAdded] = useState(false);

  const handleSizeSelect = (size) => {
    setSelectedSize(size);
    if (size === 8) {
      setShowSizeWarning(true);
    }
  };

  const switchToRecommended = () => {
    setSelectedSize(9);
    setShowSizeWarning(false);
  };

  const handleAddToCart = () => {
    if (!selectedSize) return;
    setCartAdded(true);
    window.dispatchEvent(new Event('addToCart'));
    setTimeout(() => setCartAdded(false), 3000);
  };

  return (
    <div className="bg-white min-h-screen font-sans text-[#0F1111]">
      {/* Breadcrumb */}
      <div className="max-w-[1500px] mx-auto px-5 py-2 text-[12px] text-[#565959]">
        Shoes & Handbags › Men's Shoes › <span className="text-[#c45500]">Casual Shoes</span>
      </div>

      <div className="max-w-[1500px] mx-auto px-5 flex flex-col lg:flex-row gap-6 pb-10">
        
        {/* LEFT — Product Image */}
        <div className="lg:w-[40%] flex-shrink-0">
          <div className="sticky top-4 border border-[#E7E9EC] rounded-lg p-6 bg-white flex items-center justify-center min-h-[400px]">
            <img src="/product2_shoes.jpg" alt="SPARX Shoes" className="max-h-[380px] max-w-full object-contain" />
          </div>
        </div>

        {/* CENTER — Product Details */}
        <div className="lg:w-[35%] flex-grow">
          <h1 className="text-[24px] leading-[32px] font-normal text-[#0F1111] mb-1">
            Sparx Men's SM-734 Casual Shoe | Light Weight | Durable | Comfortable | Daily Use
          </h1>

          <div className="flex items-center gap-2 mb-2">
            <span className="text-[14px] text-[#007185]">Sparx</span>
            <span className="text-[12px] text-[#565959]">Visit the Sparx Store</span>
          </div>

          {/* Rating */}
          <div className="flex items-center gap-1 mb-3">
            <span className="text-[14px] text-[#007185]">4.0</span>
            <div className="flex">
              {[1,2,3,4].map(i => <Star key={i} size={16} fill="#FFA41C" stroke="#FFA41C"/>)}
              <Star size={16} fill="#E0E0E0" stroke="#E0E0E0"/>
            </div>
            <span className="text-[14px] text-[#007185] ml-1">3,421 ratings</span>
          </div>

          <div className="border-b border-[#E7E9EC] pb-3 mb-3"></div>

          {/* Price */}
          <div className="mb-1">
            <span className="text-[12px] text-[#CC0C39] font-bold">-52%</span>
            <span className="text-[28px] ml-2 font-light">₹849</span>
          </div>
          <div className="text-[14px] text-[#565959] mb-4">
            M.R.P.: <span className="line-through">₹1,799</span>
          </div>

          {/* SIZE SELECTOR */}
          <div className="mb-6">
            <h3 className="text-[14px] font-bold mb-2 flex items-center gap-2">
              <Ruler size={16}/> Size: <span className="text-[#007185]">{selectedSize ? `UK ${selectedSize}` : 'Select'}</span>
            </h3>
            <div className="flex gap-2 flex-wrap">
              {[6, 7, 8, 9, 10].map(size => (
                <button
                  key={size}
                  onClick={() => handleSizeSelect(size)}
                  className={`w-16 h-12 rounded border-2 text-[14px] font-medium transition-all
                    ${selectedSize === size 
                      ? 'border-[#007185] bg-[#EDFDFF] text-[#007185] shadow-sm' 
                      : 'border-[#D5D9D9] bg-white hover:bg-[#F7F8F8] text-[#0F1111]'}`}
                >
                  UK {size}
                </button>
              ))}
            </div>
          </div>

          {/* About this item */}
          <div className="mb-4">
            <h3 className="text-[16px] font-bold mb-2">About this item</h3>
            <ul className="list-disc pl-5 text-[14px] text-[#333] space-y-1.5 leading-snug">
              <li>Outer Material: Mesh — lightweight and breathable</li>
              <li>Closure Type: Lace-Up</li>
              <li>Sole Material: EVA — shock-absorbing and durable</li>
              <li>Ideal for daily wear, walking, and casual outings</li>
              <li>Available in multiple colours</li>
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
            <div className="text-[28px] font-light mb-1">₹849</div>
            <div className="text-[14px] text-[#565959] mb-3">
              FREE delivery <span className="font-bold text-[#0F1111]">Tuesday, 17 June</span>
            </div>
            <div className="flex items-center text-[14px] text-[#007185] mb-4 cursor-pointer">
              <MapPin size={16} className="mr-1"/> Deliver to Chandigarh 140603
            </div>

            <div className="text-[18px] text-[#007600] font-bold mb-4">In stock</div>

            <button 
              onClick={handleAddToCart}
              disabled={!selectedSize}
              className="w-full bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-full py-2 text-[14px] font-medium mb-2 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {selectedSize ? 'Add to Cart' : 'Select a size first'}
            </button>
            <button 
              disabled={!selectedSize}
              className="w-full bg-[#FFA41C] hover:bg-[#FA8900] border border-[#FF8F00] rounded-full py-2 text-[14px] font-medium mb-4 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Buy Now
            </button>

            {cartAdded && (
              <div className="mt-3 bg-green-50 border border-green-300 text-green-800 text-[13px] p-2 rounded flex items-center">
                <ShieldCheck size={16} className="mr-2"/> Added to Cart!
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ═══ SIZE HISTORY WARNING POPUP ═══ */}
      {showSizeWarning && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-lg w-full shadow-2xl overflow-hidden">
            
            {/* Header */}
            <div className="bg-[#E3F2FD] border-b border-[#90CAF9] px-5 py-3 flex items-center justify-between">
              <div className="flex items-center">
                <Ruler size={20} className="text-[#1565C0] mr-2" />
                <h3 className="font-bold text-[16px] text-[#0F1111]">Size Recommendation Based on Your History</h3>
              </div>
              <button onClick={() => setShowSizeWarning(false)} className="text-gray-500 hover:text-black">
                <X size={18}/>
              </button>
            </div>

            <div className="p-5">
              {/* Warning */}
              <div className="bg-[#FFF3E0] border border-[#FFE0B2] rounded p-3 mb-4">
                <div className="flex items-start">
                  <AlertTriangle size={18} className="text-[#F57C00] mr-2 mt-0.5 flex-shrink-0"/>
                  <div>
                    <p className="text-[14px] font-bold text-[#E65100] mb-1">You previously returned a shoe in Size UK 8</p>
                    <p className="text-[13px] text-[#BF360C]">Order #AMZ-2026-1847 • Return reason: <strong>Size was too tight</strong></p>
                  </div>
                </div>
              </div>

              {/* Recommendation */}
              <div className="bg-[#E8F5E9] border border-[#A5D6A7] rounded p-3 mb-4">
                <p className="text-[14px] text-[#2E7D32]">
                  📏 Based on your return history, we recommend <strong className="text-[16px]">Size UK 9</strong> for this brand.
                </p>
              </div>

              {/* Size Chart */}
              <h4 className="font-bold text-[14px] mb-2">Size Chart (UK → cm)</h4>
              <table className="w-full text-[13px] mb-4 border border-[#E7E9EC]">
                <thead>
                  <tr className="bg-[#F0F2F2]">
                    <th className="p-2 text-left border-b border-[#E7E9EC]">UK Size</th>
                    <th className="p-2 text-left border-b border-[#E7E9EC]">Foot Length (cm)</th>
                    <th className="p-2 text-left border-b border-[#E7E9EC]"></th>
                  </tr>
                </thead>
                <tbody>
                  {SIZE_CHART.map(row => (
                    <tr key={row.uk} className={row.uk === 8 ? 'bg-red-50' : row.uk === 9 ? 'bg-green-50' : ''}>
                      <td className="p-2 border-b border-[#E7E9EC] font-medium">
                        UK {row.uk}
                        {row.uk === 8 && <span className="text-[11px] text-red-600 ml-2">← You returned this</span>}
                        {row.uk === 9 && <span className="text-[11px] text-green-600 ml-2">← Recommended</span>}
                      </td>
                      <td className="p-2 border-b border-[#E7E9EC]">{row.cm} cm</td>
                      <td className="p-2 border-b border-[#E7E9EC]">
                        {row.uk === 9 && <span className="text-green-600 font-bold">✓</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Actions */}
              <div className="flex gap-3">
                <button 
                  onClick={switchToRecommended}
                  className="flex-1 bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-full py-2 text-[14px] font-medium shadow-sm"
                >
                  Switch to Size UK 9
                </button>
                <button 
                  onClick={() => setShowSizeWarning(false)}
                  className="flex-1 bg-white border border-[#D5D9D9] hover:bg-[#F7F8F8] rounded-full py-2 text-[14px] font-medium shadow-sm"
                >
                  Keep Size UK 8
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
