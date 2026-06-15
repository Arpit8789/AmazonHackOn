import { useState, useRef } from 'react';
import { Star, ShieldCheck, Truck, MapPin, Search, Mic, MicOff, RefreshCw, Info } from 'lucide-react';

const REVIEWS = [
  { id: 1, user: "Rahul M.", stars: 5, title: "Amazing sound quality for the price!", body: "The sound quality is outstanding. Deep bass and clear treble. I use it daily for music and calls. Battery lasts about 10 hours on medium volume. Totally worth it.", date: "14 May 2025", keywords: ["sound quality", "bass", "battery", "music"] },
  { id: 2, user: "Priya S.", stars: 4, title: "Good battery life, decent bass", body: "Battery life is really impressive — easily lasts 10-12 hours. Bass could be a bit deeper for EDM but overall sound is balanced and good for the price range.", date: "2 May 2025", keywords: ["battery life", "bass", "battery", "sound"] },
  { id: 3, user: "Amit K.", stars: 3, title: "Build quality could be better", body: "Sound is fine but the build quality feels a bit plasticky. The buttons are hard to press sometimes. Not very durable if you drop it. For the price, it's okay.", date: "28 Apr 2025", keywords: ["build quality", "durability", "buttons", "plastic"] },
  { id: 4, user: "Sneha R.", stars: 5, title: "Perfect for outdoor use", body: "Waterproof and dustproof — I've used it at the beach and by the pool. Sound is loud enough for outdoor gatherings. Bluetooth connectivity is stable even at 10 meters.", date: "15 Apr 2025", keywords: ["waterproof", "outdoor", "bluetooth", "connectivity", "loud"] },
  { id: 5, user: "Vikram T.", stars: 2, title: "Charging port broke after 2 months", body: "The charging port became loose after about 2 months of use. Sound quality was great while it lasted. Not happy with the durability. Would not recommend for long-term use.", date: "3 Apr 2025", keywords: ["charging", "durability", "broken", "port"] },
];

// Multilingual keyword mapping (Hindi/Tamil phrases → English keywords)
const LANGUAGE_MAP = {
  "battery kitni chalti hai": "battery life",
  "battery": "battery",
  "awaz kaisi hai": "sound quality",
  "sound quality": "sound quality",
  "sound": "sound",
  "bass": "bass",
  "build quality": "build quality",
  "waterproof": "waterproof",
  "charging": "charging",
  "kitna loud hai": "loud",
  "pani mein chalega": "waterproof",
  "mazboot hai kya": "build quality",
  "durability": "durability",
  "toot jayega kya": "durability",
  "bluetooth": "bluetooth",
  "outdoor": "outdoor",
};

export default function ProductPage3() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredReviews, setFilteredReviews] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [noResults, setNoResults] = useState(false);
  const [showResellTooltip, setShowResellTooltip] = useState(false);
  const [cartAdded, setCartAdded] = useState(false);
  const searchRef = useRef(null);

  const handleSearch = (query) => {
    if (!query.trim()) {
      setFilteredReviews(null);
      setNoResults(false);
      return;
    }

    const lowerQ = query.toLowerCase().trim();
    
    // Check multilingual mapping first
    let englishKeyword = LANGUAGE_MAP[lowerQ] || lowerQ;
    
    const results = REVIEWS.filter(r => 
      r.keywords.some(k => k.includes(englishKeyword)) ||
      r.body.toLowerCase().includes(englishKeyword) ||
      r.title.toLowerCase().includes(englishKeyword)
    );

    if (results.length > 0) {
      setFilteredReviews(results);
      setNoResults(false);
    } else {
      setFilteredReviews([]);
      setNoResults(true);
    }
  };

  const handleMic = () => {
    setIsListening(true);
    setTimeout(() => {
      setIsListening(false);
      const demoQuery = "sound quality";
      setSearchQuery(demoQuery);
      handleSearch(demoQuery);
    }, 2500);
  };

  const handleAddToCart = () => {
    setCartAdded(true);
    window.dispatchEvent(new Event('addToCart'));
    setTimeout(() => setCartAdded(false), 3000);
  };

  const displayReviews = filteredReviews !== null ? filteredReviews : REVIEWS;

  return (
    <div className="bg-white min-h-screen font-sans text-[#0F1111]">
      {/* Breadcrumb */}
      <div className="max-w-[1500px] mx-auto px-5 py-2 text-[12px] text-[#565959]">
        Electronics › Audio › Speakers › <span className="text-[#c45500]">Bluetooth Speakers</span>
      </div>

      <div className="max-w-[1500px] mx-auto px-5 flex flex-col lg:flex-row gap-6 pb-6">
        
        {/* LEFT — Product Image */}
        <div className="lg:w-[40%] flex-shrink-0">
          <div className="sticky top-4 border border-[#E7E9EC] rounded-lg p-6 bg-white flex items-center justify-center min-h-[400px]">
            <img src="/product3_headphones.jpg" alt="boAt Stone 352 Pro" className="max-h-[380px] max-w-full object-contain" />
          </div>
        </div>

        {/* CENTER — Product Details */}
        <div className="lg:w-[35%] flex-grow">
          <h1 className="text-[24px] leading-[32px] font-normal text-[#0F1111] mb-1">
            boAt Stone 352 Pro Bluetooth Speaker with 14W Sound, Up to 12Hrs Playtime, IPX5 Water Resistant, TWS Feature
          </h1>

          <div className="flex items-center gap-2 mb-2">
            <span className="text-[14px] text-[#007185]">boAt</span>
            <span className="text-[12px] text-[#565959]">Visit the boAt Store</span>
          </div>

          {/* Rating */}
          <div className="flex items-center gap-1 mb-3">
            <span className="text-[14px] text-[#007185]">4.2</span>
            <div className="flex">
              {[1,2,3,4].map(i => <Star key={i} size={16} fill="#FFA41C" stroke="#FFA41C"/>)}
              <Star size={16} fill="#E0E0E0" stroke="#E0E0E0"/>
            </div>
            <span className="text-[14px] text-[#007185] ml-1">5,128 ratings</span>
          </div>

          <div className="border-b border-[#E7E9EC] pb-3 mb-3"></div>

          {/* Price */}
          <div className="mb-1">
            <span className="text-[12px] text-[#CC0C39] font-bold">-64%</span>
            <span className="text-[28px] ml-2 font-light">₹1,299</span>
          </div>
          <div className="text-[14px] text-[#565959] mb-4">
            M.R.P.: <span className="line-through">₹3,590</span>
          </div>

          {/* About this item */}
          <div className="mb-4">
            <h3 className="text-[16px] font-bold mb-2">About this item</h3>
            <ul className="list-disc pl-5 text-[14px] text-[#333] space-y-1.5 leading-snug">
              <li>14W HD sound with boAt Signature Sound</li>
              <li>Up to 12 hours of playtime on a single charge</li>
              <li>IPX5 water and splash resistant</li>
              <li>TWS feature to pair two speakers for stereo sound</li>
              <li>Bluetooth v5.3 for stable connectivity</li>
              <li>Manufacturer Warranty: 1 year from date of purchase</li>
            </ul>
          </div>

          {/* Return & Replacement Policy — with RESELL AVAILABLE */}
          <div className="border border-[#E7E9EC] rounded p-4 relative">
            <h3 className="text-[16px] font-bold mb-2">Return, Replacement & Refund Policy</h3>
            <div className="text-[14px] text-[#565959] space-y-2">
              <div className="flex items-center gap-2">
                <ShieldCheck size={16} className="text-[#007185]"/>
                <span>10 days return / replacement</span>
              </div>
              <div className="flex items-center gap-2">
                <Truck size={16} className="text-[#007185]"/>
                <span>Free delivery by Amazon</span>
              </div>
              
              {/* RESELL AVAILABLE */}
              <div className="relative">
                <div 
                  className="flex items-center gap-2 cursor-pointer"
                  onMouseEnter={() => setShowResellTooltip(true)}
                  onMouseLeave={() => setShowResellTooltip(false)}
                >
                  <RefreshCw size={16} className="text-green-600"/>
                  <span className="text-green-700 font-medium">Resell Available ✓</span>
                  <Info size={14} className="text-[#565959]"/>
                </div>

                {/* Resell Tooltip */}
                {showResellTooltip && (
                  <div className="absolute bottom-full left-0 mb-2 w-[340px] bg-[#0F1111] text-white rounded-lg p-4 shadow-xl z-50">
                    <div className="text-[13px] leading-relaxed">
                      <p className="font-bold mb-2 text-[14px]">Amazon Second Life — Resell Policy</p>
                      <p className="mb-2 text-gray-300">You can resell this product on Amazon Second Life if:</p>
                      <ul className="space-y-1.5 mb-3">
                        <li className="flex items-start gap-1.5">
                          <span className="text-green-400 mt-0.5">✔</span>
                          <span>At least <strong>25% of warranty remains</strong> OR minimum <strong>2 months</strong> warranty available</span>
                        </li>
                        <li className="flex items-start gap-1.5">
                          <span className="text-green-400 mt-0.5">✔</span>
                          <span>Product is in <strong>working / functional</strong> condition</span>
                        </li>
                      </ul>
                      <p className="text-gray-400 text-[12px] border-t border-gray-700 pt-2">
                        <strong className="text-gray-300">Transparent charges:</strong> Packaging fee + Logistics cost + Platform Fee. All charges are shown upfront before you list.
                      </p>
                    </div>
                    <div className="absolute -bottom-1.5 left-6 w-3 h-3 bg-[#0F1111] rotate-45"></div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT — Buy Box */}
        <div className="lg:w-[25%] flex-shrink-0">
          <div className="border border-[#D5D9D9] rounded-lg p-5 sticky top-4">
            <div className="text-[28px] font-light mb-1">₹1,299</div>
            <div className="text-[14px] text-[#565959] mb-3">
              FREE delivery <span className="font-bold text-[#0F1111]">Monday, 16 June</span>
            </div>
            <div className="flex items-center text-[14px] text-[#007185] mb-4 cursor-pointer">
              <MapPin size={16} className="mr-1"/> Deliver to Chandigarh 140603
            </div>

            <div className="text-[18px] text-[#007600] font-bold mb-4">In stock</div>

            <button 
              onClick={handleAddToCart}
              className="w-full bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-full py-2 text-[14px] font-medium mb-2 shadow-sm"
            >
              Add to Cart
            </button>
            <button className="w-full bg-[#FFA41C] hover:bg-[#FA8900] border border-[#FF8F00] rounded-full py-2 text-[14px] font-medium mb-4 shadow-sm">
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

      {/* ═══ CUSTOMER REVIEWS SECTION ═══ */}
      <div className="max-w-[1500px] mx-auto px-5 pb-10 border-t border-[#E7E9EC] pt-6">
        <div className="flex flex-col lg:flex-row gap-8">
          
          {/* Left: Rating Summary */}
          <div className="lg:w-[280px] flex-shrink-0">
            <h2 className="text-[22px] font-bold mb-3">Customer reviews</h2>
            <div className="flex items-center gap-2 mb-2">
              <div className="flex">
                {[1,2,3,4].map(i => <Star key={i} size={18} fill="#FFA41C" stroke="#FFA41C"/>)}
                <Star size={18} fill="#E0E0E0" stroke="#E0E0E0"/>
              </div>
              <span className="text-[16px] font-medium">4.2 out of 5</span>
            </div>
            <p className="text-[14px] text-[#565959] mb-4">5,128 global ratings</p>

            {/* Star breakdown */}
            {[
              { stars: 5, pct: 58 },
              { stars: 4, pct: 22 },
              { stars: 3, pct: 10 },
              { stars: 2, pct: 5 },
              { stars: 1, pct: 5 },
            ].map(row => (
              <div key={row.stars} className="flex items-center gap-2 mb-1.5 text-[13px]">
                <span className="text-[#007185] w-12 cursor-pointer hover:underline">{row.stars} star</span>
                <div className="flex-1 bg-[#E7E9EC] rounded-full h-[18px] overflow-hidden">
                  <div className="bg-[#FFA41C] h-full rounded-full" style={{width: `${row.pct}%`}}></div>
                </div>
                <span className="text-[#007185] w-8 text-right cursor-pointer hover:underline">{row.pct}%</span>
              </div>
            ))}
          </div>

          {/* Right: Review Search + List */}
          <div className="flex-1">
            {/* Search Bar */}
            <div className="mb-4">
              <h3 className="text-[16px] font-bold mb-2">Search reviews — Ask in any language</h3>
              <div className="flex items-center border border-[#D5D9D9] rounded-lg overflow-hidden shadow-sm">
                <div className="px-3 text-[#565959]">
                  <Search size={18}/>
                </div>
                <input
                  ref={searchRef}
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSearch(searchQuery)}
                  placeholder="Search reviews (e.g. 'battery kitni chalti hai', 'sound quality')"
                  className="flex-1 py-2.5 text-[14px] focus:outline-none"
                />
                <button 
                  onClick={() => handleSearch(searchQuery)}
                  className="px-3 py-2.5 bg-[#F0F2F2] hover:bg-[#E3E6E6] border-l border-[#D5D9D9] text-[13px] font-medium"
                >
                  Search
                </button>
                <button 
                  onClick={handleMic}
                  className={`px-3 py-2.5 border-l border-[#D5D9D9] transition-colors ${isListening ? 'bg-red-50 text-red-500' : 'text-[#565959] hover:text-[#0F1111]'}`}
                  title="Voice search"
                >
                  {isListening ? <MicOff size={18} className="animate-pulse"/> : <Mic size={18}/>}
                </button>
              </div>
              {isListening && (
                <div className="mt-2 text-[13px] text-red-500 flex items-center">
                  <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse mr-2"></div>
                  Listening... Speak now
                </div>
              )}
            </div>

            {/* Quick Search Pills */}
            <div className="flex flex-wrap gap-2 mb-4">
              {["Battery Life", "Sound Quality", "Build Quality", "Waterproof"].map(pill => (
                <button
                  key={pill}
                  onClick={() => { setSearchQuery(pill); handleSearch(pill); }}
                  className="border border-[#D5D9D9] rounded-full px-3 py-1 text-[13px] text-[#007185] hover:bg-[#F0F2F2] transition-colors"
                >
                  {pill}
                </button>
              ))}
            </div>

            {/* No Results */}
            {noResults && (
              <div className="bg-[#FFF8E1] border border-[#FFE082] rounded p-3 mb-4 text-[14px] text-[#795548]">
                No reviews found related to your query. Try different keywords.
              </div>
            )}

            {/* Reviews List */}
            <div className="space-y-4">
              {displayReviews.map(review => (
                <div key={review.id} className="border-b border-[#E7E9EC] pb-4">
                  <div className="flex items-center gap-2 mb-1">
                    <div className="w-8 h-8 rounded-full bg-[#E7E9EC] flex items-center justify-center text-[14px] font-bold">
                      {review.user[0]}
                    </div>
                    <span className="text-[13px] text-[#0F1111]">{review.user}</span>
                  </div>
                  <div className="flex items-center gap-1 mb-1">
                    {Array.from({length: 5}).map((_, i) => (
                      <Star key={i} size={14} fill={i < review.stars ? "#FFA41C" : "#E0E0E0"} stroke={i < review.stars ? "#FFA41C" : "#E0E0E0"}/>
                    ))}
                    <span className="text-[14px] font-bold ml-1">{review.title}</span>
                  </div>
                  <div className="text-[12px] text-[#565959] mb-1">Reviewed in India on {review.date}</div>
                  <p className="text-[14px] text-[#333] leading-snug">{review.body}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
