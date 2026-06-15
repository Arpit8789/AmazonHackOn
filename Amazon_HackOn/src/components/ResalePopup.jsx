import { useState, useRef } from 'react';
import { IndianRupee, MapPin, AlertTriangle, ShieldCheck, X, Camera, CheckCircle, Package, TrendingUp, TrendingDown, Sparkles } from 'lucide-react';
import { apiService } from '../api/api';

export default function ResalePopup({ order, onClose }) {
  const [step, setStep] = useState(1);
  
  // Step 1 State: Upload & Description
  const [uploadedFiles, setUploadedFiles] = useState({});
  const [uploadedPreviews, setUploadedPreviews] = useState({});
  const [description, setDescription] = useState("");
  const [isAssessing, setIsAssessing] = useState(false);
  const fileInputRef = useRef(null);

  // AI Assessment result
  const [aiResult, setAiResult] = useState(null);

  // Step 2 State: Coverage & Pricing
  const [coverage, setCoverage] = useState("same_city");

  // Derived pricing (set after AI assessment)
  const baseAiValuation = aiResult?.prediction?.predicted_resale_price || Math.round(order.original_price * 0.45);
  const minPrice = Math.round(baseAiValuation * 0.85);
  const maxPrice = Math.round(baseAiValuation * 1.25);
  
  const [sellerPrice, setSellerPrice] = useState(null); // set after AI result

  // Logistics mapping
  const logisticsCosts = {
    same_city: 50,
    near_city: 80,
    same_state: 120,
    near_state: 180,
    pan_india: 250
  };

  const logisticsCost = logisticsCosts[coverage];
  const packagingCost = 30;
  const currentSellerPrice = sellerPrice ?? baseAiValuation;
  const platformFee = Math.round(baseAiValuation * 0.08);
  const finalPayout = currentSellerPrice - platformFee - logisticsCost - packagingCost;

  const [isListing, setIsListing] = useState(false);

  const handlePhotoUpload = (index, e) => {
    const file = e.target.files[0];
    if (file) {
      setUploadedFiles(prev => ({ ...prev, [index]: file }));
      setUploadedPreviews(prev => ({ ...prev, [index]: URL.createObjectURL(file) }));
    }
  };

  const runAIAssessment = async () => {
    setIsAssessing(true);

    try {
      const formData = new FormData();
      Object.values(uploadedFiles).forEach(file => {
        formData.append("images", file);
      });
      formData.append("description", description);
      formData.append("product_category", order.product_category || "Electronics");
      formData.append("brand", "Unknown");
      formData.append("product_name", order.product_name || "Unknown Product");
      formData.append("purchase_price", order.original_price);
      formData.append("current_market_price", order.original_price);
      formData.append("purchase_date", order.purchase_date || "2026-01-01");
      formData.append("initial_warranty_days", (order.warranty_months || 12) * 30);

      const result = await apiService.getAiResalePrice(formData);
      console.log("=== AI Grade Response ===", result);
      setAiResult(result);
      setSellerPrice(Math.round(result.prediction.predicted_resale_price));
    } catch (err) {
      console.error("AI assessment failed:", err);
      // Use fallback values
      setAiResult({
        ai_grading_report: {
          condition_score: 70,
          condition_grade: "B",
          gemini_report: {
            inspection_summary: "Basic assessment applied.",
          }
        },
        prediction: {
          predicted_resale_price: Math.round(order.original_price * 0.45),
          confidence_score: 50,
          top_positive_factors: ["Product appears functional"],
          top_negative_factors: ["Could not fully assess via AI"],
        }
      });
      setSellerPrice(Math.round(order.original_price * 0.45));
    }

    setIsAssessing(false);
    setStep(2);
  };

  const handleConfirmList = async () => {
    setIsListing(true);
    try {
      await apiService.submitResale({
        product_id: order?.product_id || order?.id || order?.order_id || "demo_prod_123",
        seller_id: "user_123",
        price_confirmed: currentSellerPrice,
        delivery_zone: coverage
      });
      setStep(3);
    } catch (error) {
      console.error("Failed to list item:", error);
    } finally {
      setIsListing(false);
    }
  };

  const gradeColor = (grade) => {
    if (grade === "A") return "text-green-700 bg-green-100 border-green-300";
    if (grade === "B") return "text-amber-700 bg-amber-100 border-amber-300";
    return "text-red-700 bg-red-100 border-red-300";
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 z-50 flex items-center justify-center p-4 font-sans text-[#0F1111]">
      <div className="bg-white rounded-2xl max-w-2xl w-full shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="bg-[#f0f2f2] border-b border-[#D5D9D9] px-5 py-3 flex justify-between items-center">
          <h2 className="text-lg font-bold">
            Resell on Amazon Second Life
          </h2>
          <button onClick={onClose} className="text-gray-500 hover:text-black focus:outline-none">
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto">
          
          {/* Product Header (Always visible except success) */}
          {step !== 3 && (
            <div className="flex gap-4 mb-6 pb-4 border-b border-[#E7E9EC]">
              <div className="w-16 h-16 bg-white border border-[#D5D9D9] rounded-xl p-1 flex-shrink-0">
                <img src={order.image_url} alt={order.product_name} className="w-full h-full object-contain mix-blend-multiply" />
              </div>
              <div>
                <h3 className="font-bold text-[15px] line-clamp-1">{order.product_name}</h3>
                <p className="text-[13px] text-[#565959]">Original Price: ₹{order.original_price} • Purchased: {order.purchase_date}</p>
              </div>
            </div>
          )}

          {/* STEP 1: UPLOAD & DESCRIBE */}
          {step === 1 && (
            <div className="space-y-6">
              <div>
                <h4 className="font-bold text-[15px] mb-2">1. Upload Current Photos</h4>
                <p className="text-[13px] text-[#565959] mb-3">Try to upload 3 to 4 images from all dimensions for getting correct resale and return evaluation.</p>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
                  {[1, 2, 3, 4].map(idx => (
                    <div 
                      key={idx}
                      className={`border-2 border-dashed ${uploadedPreviews[idx] ? 'border-green-500 bg-green-50' : 'border-[#D5D9D9] bg-[#f7f8f8] hover:bg-[#f0f2f2]'} rounded-xl p-3 flex flex-col items-center justify-center cursor-pointer transition-colors h-28 relative overflow-hidden group`}
                    >
                      {uploadedPreviews[idx] ? (
                        <>
                          <img src={uploadedPreviews[idx]} alt={`Uploaded ${idx}`} className="absolute inset-0 w-full h-full object-cover" />
                          <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                            <span className="text-white font-bold text-[10px] bg-black px-2 py-1 rounded">Change</span>
                          </div>
                        </>
                      ) : (
                        <>
                          <Camera size={20} className="text-[#565959] mb-1" />
                          <span className="text-[11px] font-bold text-center">Image {idx}{idx === 4 ? ' (Optional)' : ''}</span>
                        </>
                      )}
                      <input 
                        type="file" 
                        accept="image/*" 
                        capture="environment"
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        onChange={(e) => handlePhotoUpload(idx, e)}
                      />
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-bold text-[15px] mb-2">2. Item Description</h4>
                <textarea 
                  className="w-full border border-[#D5D9D9] rounded-xl p-3 text-[14px] focus:outline-none focus:border-[#007185] focus:ring-1 focus:ring-[#007185] shadow-inner"
                  rows="3"
                  placeholder="Describe the current condition (e.g., lightly used, minor scratch on back, fully functional)..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                ></textarea>
              </div>

              <div className="flex justify-end pt-2">
                <button 
                  onClick={runAIAssessment}
                  disabled={Object.keys(uploadedFiles).length < 3 || !description.trim() || isAssessing}
                  className="bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-xl px-8 py-2 text-[14px] shadow-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                >
                  {isAssessing ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-[#0F1111] mr-2"></div>
                      AI Assessing Value...
                    </>
                  ) : "Assess Resale Value"}
                </button>
              </div>
            </div>
          )}

          {/* STEP 2: AI RESULT + PRICING & LOGISTICS */}
          {step === 2 && aiResult && (
            <div className="space-y-5">
              
              {/* AI Pricing Factors */}
              <div className="bg-[#F0F8FF] border border-[#b2d5d8] rounded-xl p-4">
                <h4 className="font-bold text-[14px] text-[#007185] mb-2 flex items-center">
                  <Sparkles size={16} className="mr-2" />
                  AI Price Analysis
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h5 className="text-[12px] font-bold text-green-700 mb-1 flex items-center">
                      <TrendingUp size={12} className="mr-1" /> Positive Value Impacts
                    </h5>
                    <ul className="space-y-1">
                      {aiResult.prediction.top_positive_factors?.slice(0,4).map((factor, i) => (
                        <li key={i} className="text-[11px] text-gray-700 capitalize">
                          <span className="text-green-600 mr-1">✓</span> 
                          {factor.replace(/(num__|cat__)/g, '').replace(/_/g, ' ')}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h5 className="text-[12px] font-bold text-red-700 mb-1 flex items-center">
                      <TrendingDown size={12} className="mr-1" /> Negative Value Impacts
                    </h5>
                    <ul className="space-y-1">
                      {aiResult.prediction.top_negative_factors?.slice(0,4).map((factor, i) => (
                        <li key={i} className="text-[11px] text-gray-700 capitalize">
                          <span className="text-red-600 mr-1">✗</span> 
                          {factor.replace(/(num__|cat__)/g, '').replace(/_/g, ' ')}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Left Col: Coverage */}
                <div>
                  <h4 className="font-bold text-[15px] mb-3 border-b border-[#D5D9D9] pb-1">1. Delivery Coverage</h4>
                  <p className="text-[10px] text-[#565959] mb-3 leading-tight italic">Delivery cost is calculated by product weight multiplied by distance/transit travel.</p>
                  
                  <div className="space-y-2">
                    {[
                      { id: 'same_city', label: 'Same City', cost: 50 },
                      { id: 'near_city', label: 'Near City', cost: 80 },
                      { id: 'same_state', label: 'Same State', cost: 120 },
                      { id: 'near_state', label: 'Near State', cost: 180 },
                      { id: 'pan_india', label: 'PAN India', cost: 250 },
                    ].map(opt => (
                      <label key={opt.id} className={`flex items-center p-2 rounded-xl border cursor-pointer transition-colors ${coverage === opt.id ? 'border-[#007185] bg-[#F0F8FF]' : 'border-[#D5D9D9] hover:bg-[#f7f8f8]'}`}>
                        <input 
                          type="radio" 
                          name="coverage" 
                          value={opt.id} 
                          checked={coverage === opt.id}
                          onChange={(e) => setCoverage(e.target.value)}
                          className="w-4 h-4 text-[#007185] focus:ring-[#007185] accent-[#007185]"
                        />
                        <span className="ml-2 text-[14px] flex-1">{opt.label}</span>
                        <span className="text-[13px] text-[#565959]">₹{opt.cost}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Right Col: Pricing */}
                <div>
                  <h4 className="font-bold text-[15px] mb-3 border-b border-[#D5D9D9] pb-1">2. Set Your Price</h4>
                  
                  <div className="mb-4">
                    <div className="flex justify-between text-[12px] text-[#565959] mb-1 font-bold">
                      <span>Min: ₹{minPrice}</span>
                      <span>Max: ₹{maxPrice}</span>
                    </div>
                    <input 
                      type="range" 
                      min={minPrice} 
                      max={maxPrice} 
                      value={currentSellerPrice} 
                      onChange={(e) => setSellerPrice(Number(e.target.value))}
                      className="w-full h-2 bg-[#D5D9D9] rounded-lg appearance-none cursor-pointer accent-[#007185]"
                    />
                    <div className="mt-2 text-center">
                      <span className="text-[12px] text-[#565959]">Selling Price:</span>
                      <span className="text-[20px] font-bold text-[#B12704] ml-2">₹{currentSellerPrice}</span>
                    </div>
                  </div>

                  <div className="bg-[#f7f8f8] border border-[#D5D9D9] rounded-xl p-4">
                    <h5 className="font-bold text-[13px] mb-2 text-[#0F1111]">Financial Breakdown</h5>
                    
                    <div className="flex justify-between items-center mb-1 text-[13px]">
                      <span className="text-[#565959]">Platform Fee</span>
                      <span className="text-[#B12704]">- ₹{platformFee}</span>
                    </div>
                    <div className="flex justify-between items-center mb-1 text-[13px]">
                      <span className="text-[#565959]">Packaging Cost</span>
                      <span className="text-[#B12704]">- ₹{packagingCost}</span>
                    </div>
                    <div className="flex justify-between items-center mb-2 text-[13px]">
                      <span className="text-[#565959]">Logistics ({coverage.replace('_', ' ')})</span>
                      <span className="text-[#B12704]">- ₹{logisticsCost}</span>
                    </div>
                    
                    <div className="border-t border-[#D5D9D9] pt-2 mt-2 flex justify-between items-center">
                      <span className="font-bold text-[14px]">Your Final Payout</span>
                      <span className="font-bold text-[18px] text-[#007185]">₹{finalPayout}</span>
                    </div>
                  </div>
                  
                  {/* Warning */}
                  <div className="flex items-start mt-4 bg-orange-50 border border-orange-200 p-3 rounded-xl">
                    <AlertTriangle size={16} className="text-orange-700 mr-2 mt-0.5 flex-shrink-0" />
                    <p className="text-[11px] text-orange-800 leading-tight">
                      Amazon bears zero loss. A penalty applies if the item condition is misrepresented during pickup verification.
                    </p>
                  </div>
                </div>

              </div>

              <div className="flex justify-end pt-4 border-t border-[#D5D9D9] mt-6 gap-3">
                <button 
                  onClick={() => setStep(1)} 
                  className="px-4 py-2 hover:bg-[#f7f8f8] rounded-xl text-[14px] font-medium border border-[#D5D9D9] shadow-sm"
                >
                  Back
                </button>
                <button 
                  onClick={handleConfirmList}
                  disabled={isListing || finalPayout < 0}
                  className="bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-xl px-8 py-2 text-[14px] shadow-sm font-medium disabled:opacity-50 flex items-center"
                >
                  {isListing ? "Listing Product..." : "Confirm & List on Amazon"}
                </button>
              </div>
            </div>
          )}

          {/* STEP 3: SUCCESS */}
          {step === 3 && (
            <div className="text-center py-10">
              <ShieldCheck size={72} className="text-[#007185] mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-2">Item Listed Successfully!</h3>
              <p className="text-[#565959] text-[14px] mb-2 max-w-md mx-auto">
                Your product is now live on the Amazon Second Life store. We are finding a buyer for you.
              </p>
              <p className="text-[#565959] text-[13px] mb-8 max-w-md mx-auto">
                Keep the item safely at home (zero storage cost). We will notify you when a buyer purchases it.
              </p>
              <button 
                onClick={onClose} 
                className="bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-xl px-8 py-2 text-[14px] shadow-sm font-medium"
              >
                Return to Orders
              </button>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
