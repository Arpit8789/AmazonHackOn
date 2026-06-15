import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { ChevronRight, Calculator, IndianRupee, MapPin, Truck, HelpCircle, FileText, CheckCircle, AlertTriangle } from 'lucide-react';
import { apiService } from '../api/api';

const SellFlow = () => {
  const [step, setStep] = useState(1);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [deliveryZone, setDeliveryZone] = useState("city");
  const [priceData, setPriceData] = useState(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [listingData, setListingData] = useState(null);

  // 1. Fetch products
  const { data: products, isLoading: loadingProducts } = useQuery({
    queryKey: ['demo-products'],
    queryFn: apiService.getProducts,
  });

  // 2. Pricing mutation
  const priceMutation = useMutation({
    mutationFn: apiService.getPrice,
    onSuccess: (data) => {
      setPriceData(data);
      setIsCalculating(false);
      setStep(2);
    }
  });

  // 3. Submit listing mutation
  const submitMutation = useMutation({
    mutationFn: apiService.submitResale,
    onSuccess: (data) => {
      setListingData(data);
      setStep(4);
    }
  });

  const handleSelectProduct = (product) => {
    setSelectedProduct(product);
    calculatePrice(product, deliveryZone);
  };

  const calculatePrice = (product, zone) => {
    setIsCalculating(true);
    
    // Calculate mock warranty percentage based on age (for demo purposes)
    const ageDays = 180;
    const totalWarrantyDays = product.warranty_months * 30;
    const remainingDays = Math.max(0, totalWarrantyDays - ageDays);
    const warrantyPercent = Math.round((remainingDays / totalWarrantyDays) * 100);

    // Call API
    setTimeout(() => {
      priceMutation.mutate({
        warranty_remaining_percent: warrantyPercent,
        original_price: product.original_price,
        product_category: product.category,
        product_age_days: ageDays,
        weight_kg: product.weight_kg,
        delivery_zone: zone,
        demand_score: 0.8
      });
    }, 1500); // 1.5s delay to simulate AI processing
  };

  const handleZoneChange = (e) => {
    const newZone = e.target.value;
    setDeliveryZone(newZone);
    if (selectedProduct) {
      calculatePrice(selectedProduct, newZone);
    }
  };

  const proceedToListing = () => {
    setStep(3);
  };

  const confirmListing = () => {
    // Calculate mock warranty percentage
    const ageDays = 180;
    const totalWarrantyDays = selectedProduct.warranty_months * 30;
    const warrantyPercent = Math.round((Math.max(0, totalWarrantyDays - ageDays) / totalWarrantyDays) * 100);

    submitMutation.mutate({
      product_id: selectedProduct.product_id,
      price_confirmed: priceData.price_high,
      delivery_zone: deliveryZone,
      warranty_remaining_percent: warrantyPercent
    });
  };

  // Helper to determine if a product is eligible
  const checkEligibility = (product) => {
    // For demo, we just use the flag set in the mock data
    return product.resale_eligible !== false;
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Breadcrumbs */}
      <div className="flex items-center text-sm text-gray-500 mb-6 flex-wrap">
        <span className={step >= 1 ? "font-bold text-black" : ""}>Your Purchases</span>
        <ChevronRight size={16} className="mx-2" />
        <span className={step >= 2 ? "font-bold text-black" : ""}>AI Pricing</span>
        <ChevronRight size={16} className="mx-2" />
        <span className={step >= 3 ? "font-bold text-black" : ""}>Review Listing</span>
        <ChevronRight size={16} className="mx-2" />
        <span className={step >= 4 ? "font-bold text-black" : ""}>Success</span>
      </div>

      {/* Step 1: Select Purchase */}
      {step === 1 && (
        <div className="bg-white p-6 border border-gray-200 rounded-sm shadow-sm">
          <div className="flex justify-between items-end mb-6 border-b border-gray-200 pb-4">
            <div>
              <h1 className="text-2xl font-bold">Resell Your Products</h1>
              <p className="text-gray-600 mt-1">Select an item from your past orders to securely resell on Amazon Second Life.</p>
            </div>
            <div className="hidden sm:block text-sm bg-[#F0F8FF] text-[#007185] px-3 py-1 border border-[#b2d5d8] rounded">
              <span className="font-bold">Zero Platform Storage Cost</span>
            </div>
          </div>

          {loadingProducts ? (
            <p className="py-8 text-center text-gray-500">Loading your purchase history...</p>
          ) : (
            <div className="space-y-6">
              {products?.map((product) => {
                const isEligible = checkEligibility(product);
                return (
                  <div key={product.product_id} className={`border p-4 rounded flex flex-col md:flex-row gap-6 relative ${isEligible ? 'border-gray-300 hover:shadow-md transition-shadow' : 'border-gray-200 opacity-60 bg-gray-50'}`}>
                    <div className="w-32 h-32 flex-shrink-0 bg-white p-2 border border-gray-100 flex items-center justify-center">
                      <img src={product.image_url} alt={product.name} className="max-w-full max-h-full object-contain" />
                    </div>
                    
                    <div className="flex-grow">
                      <div className="flex justify-between items-start">
                        <h3 className="font-bold text-lg text-black">
                          {product.name}
                        </h3>
                        {/* Eligibility Badge */}
                        {isEligible ? (
                          <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded-sm border border-green-200">
                            Eligible for Resale
                          </span>
                        ) : (
                          <span className="bg-red-100 text-red-800 text-xs font-bold px-2 py-1 rounded-sm border border-red-200">
                            Not Eligible
                          </span>
                        )}
                      </div>
                      
                      <div className="text-sm text-gray-600 mt-1 mb-2">Purchased: {product.purchase_date}</div>
                      
                      <div className="grid grid-cols-2 gap-4 max-w-sm mt-4 text-sm">
                        <div>
                          <div className="text-gray-500">Original Price</div>
                          <div className="font-bold">₹{product.original_price}</div>
                        </div>
                        <div>
                          <div className="text-gray-500">Warranty</div>
                          <div className="font-bold">{product.warranty_months} months</div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex flex-col justify-center min-w-[200px] border-l border-gray-200 pl-4">
                      {isEligible ? (
                        <>
                          <button 
                            onClick={() => handleSelectProduct(product)}
                            className="btn-yellow w-full py-2 flex justify-center items-center font-bold"
                            disabled={isCalculating}
                          >
                            <Calculator size={18} className="mr-2" />
                            Calculate Price
                          </button>
                          <p className="text-xs text-center mt-3 text-gray-500 flex items-center justify-center">
                            <HelpCircle size={12} className="mr-1" />
                            AI calculates best market price
                          </p>
                        </>
                      ) : (
                        <div className="text-sm text-red-600 bg-red-50 p-2 rounded text-center">
                          <AlertTriangle size={16} className="inline mr-1" />
                          Warranty expired. Product no longer eligible for P2P resale.
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Loading Overlay */}
      {isCalculating && (
        <div className="fixed inset-0 bg-white bg-opacity-90 z-50 flex flex-col items-center justify-center">
          <div className="w-16 h-16 border-4 border-[#007185] border-t-transparent rounded-full animate-spin mb-4"></div>
          <h2 className="text-xl font-bold text-[#007185] mb-2">AI Analyzing Market Data...</h2>
          <p className="text-sm text-gray-500 max-w-sm text-center">
            Calculating optimal resale price based on remaining warranty, current regional demand, and category sell-through rates.
          </p>
        </div>
      )}

      {/* Step 2: AI Pricing */}
      {step === 2 && priceData && selectedProduct && (
        <div className="bg-white p-6 border border-gray-200 rounded-sm shadow-sm">
          <h1 className="text-2xl font-bold mb-6">Set Your Resale Terms</h1>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column: Product & Delivery */}
            <div className="lg:col-span-1 space-y-6">
              <div className="border border-gray-200 p-4 rounded-sm">
                <div className="flex items-center space-x-4 mb-4">
                  <img src={selectedProduct.image_url} alt={selectedProduct.name} className="w-16 h-16 object-contain" />
                  <div className="font-bold text-sm line-clamp-2">{selectedProduct.name}</div>
                </div>
                <div className="text-xs text-gray-500 border-t pt-2">Original Price: ₹{selectedProduct.original_price}</div>
              </div>

              <div className="border border-gray-200 p-4 rounded-sm bg-gray-50">
                <h3 className="font-bold mb-3 flex items-center">
                  <MapPin size={18} className="text-[#007185] mr-2" />
                  Select Delivery Range
                </h3>
                <p className="text-xs text-gray-600 mb-4">
                  How far are you willing to ship? Wider range increases sale probability but increases delivery charge for the buyer.
                </p>
                
                <div className="space-y-2">
                  <label className="flex items-center p-2 border rounded cursor-pointer hover:bg-white bg-white">
                    <input type="radio" name="zone" value="local" checked={deliveryZone === 'local'} onChange={handleZoneChange} className="mr-3" />
                    <span className="text-sm font-medium">Local (Same city)</span>
                  </label>
                  <label className="flex items-center p-2 border rounded cursor-pointer hover:bg-white bg-white">
                    <input type="radio" name="zone" value="city" checked={deliveryZone === 'city'} onChange={handleZoneChange} className="mr-3" />
                    <span className="text-sm font-medium">Nearby Cities</span>
                  </label>
                  <label className="flex items-center p-2 border rounded cursor-pointer hover:bg-white bg-white">
                    <input type="radio" name="zone" value="regional" checked={deliveryZone === 'regional'} onChange={handleZoneChange} className="mr-3" />
                    <span className="text-sm font-medium">Regional (Same state)</span>
                  </label>
                </div>
              </div>
            </div>

            {/* Right Column: AI Pricing & Breakdown */}
            <div className="lg:col-span-2 space-y-6">
              
              {/* SHAP Explanation Card */}
              <div className="border border-[#b2d5d8] rounded-sm overflow-hidden shadow-sm">
                <div className="bg-[#F0F8FF] p-4 border-b border-[#b2d5d8]">
                  <h3 className="font-bold text-lg text-[#007185] flex items-center">
                    <IndianRupee size={20} className="mr-2" />
                    AI Price Explanation
                  </h3>
                  <p className="text-xs text-gray-600 mt-1">How our AI determined your product's value.</p>
                </div>
                
                <div className="p-4 bg-white">
                  <div className="space-y-3">
                    {priceData.shap_explanation.map((item, idx) => (
                      <div key={idx} className="flex justify-between items-center text-sm border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                        <span className="text-gray-700">{item.factor}</span>
                        <span className={`font-bold ${item.direction === 'positive' ? 'text-green-600' : item.direction === 'negative' ? 'text-red-600' : 'text-gray-600'}`}>
                          {item.impact_inr}
                        </span>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 pt-4 border-t border-gray-200 flex justify-between items-center">
                    <span className="font-bold">Calculated Base Value</span>
                    <span className="text-xl font-bold">₹{priceData.predicted_value}</span>
                  </div>
                </div>
              </div>

              {/* Breakdown Table */}
              <div className="border border-gray-200 rounded-sm">
                <div className="bg-gray-100 p-3 border-b border-gray-200">
                  <h3 className="font-bold text-sm">Transparent Price Breakdown</h3>
                </div>
                <div className="p-4">
                  <table className="w-full text-sm">
                    <tbody>
                      <tr className="border-b">
                        <td className="py-2 text-gray-600">Base Resale Value</td>
                        <td className="py-2 text-right font-bold">{priceData.breakdown.resale_value}</td>
                      </tr>
                      <tr className="border-b">
                        <td className="py-2 text-gray-600 flex items-center">
                          Packaging Cost
                          <HelpCircle size={12} className="ml-1 text-gray-400" />
                        </td>
                        <td className="py-2 text-right">+ ₹{priceData.breakdown.packaging_cost}</td>
                      </tr>
                      <tr className="border-b">
                        <td className="py-2 text-gray-600">Reprocessing Charge</td>
                        <td className="py-2 text-right">+ ₹{priceData.breakdown.reprocessing_charge}</td>
                      </tr>
                      <tr className="border-b">
                        <td className="py-2 text-gray-600">Amazon Platform Fee</td>
                        <td className="py-2 text-right">+ ₹{priceData.breakdown.amazon_platform_fee_7pct}</td>
                      </tr>
                      <tr className="border-b bg-[#F0F8FF]">
                        <td className="py-2 text-[#007185] font-medium flex items-center pl-2">
                          <Truck size={14} className="mr-2" />
                          Delivery ({priceData.breakdown.delivery_zone})
                        </td>
                        <td className="py-2 text-right font-medium text-[#007185] pr-2">+ ₹{priceData.breakdown.delivery_charge}</td>
                      </tr>
                      <tr className="border-b-2 border-black">
                        <td className="py-3 font-bold text-base">Final Listed Price for Buyer</td>
                        <td className="py-3 text-right font-bold text-base">₹{priceData.final_price_to_buyer_low} — ₹{priceData.final_price_to_buyer_high}</td>
                      </tr>
                      <tr className="bg-green-50">
                        <td className="py-3 font-bold text-green-800 pl-2">You Receive (After Sale)</td>
                        <td className="py-3 text-right font-bold text-xl text-green-800 pr-2">₹{priceData.seller_receives}</td>
                      </tr>
                    </tbody>
                  </table>
                  
                  <div className="mt-6 flex justify-between items-center">
                    <button onClick={() => setStep(1)} className="text-[#007185] hover:underline text-sm font-bold">
                      &lsaquo; Back to items
                    </button>
                    <button onClick={proceedToListing} className="btn-yellow px-8 py-2.5 font-bold shadow-sm">
                      Review Listing
                    </button>
                  </div>
                </div>
              </div>
              
            </div>
          </div>
        </div>
      )}

      {/* Step 3: Review Listing Preview */}
      {step === 3 && priceData && selectedProduct && (
        <div className="bg-white p-6 border border-gray-200 rounded-sm shadow-sm max-w-3xl mx-auto">
          <h1 className="text-2xl font-bold mb-6 flex items-center">
            <FileText className="mr-3 text-[#007185]" />
            Preview Your Listing
          </h1>
          
          {/* Mock Amazon Product Page */}
          <div className="border border-gray-300 rounded overflow-hidden">
            <div className="bg-gray-100 px-4 py-2 border-b border-gray-300 text-xs text-gray-500 font-bold uppercase tracking-wider flex justify-between">
              <span>Preview — How buyers will see your item</span>
              <span className="text-amazon-orange">Amazon Second Life</span>
            </div>
            
            <div className="p-6 flex flex-col md:flex-row gap-8">
              {/* Image side */}
              <div className="w-full md:w-1/3 flex flex-col items-center">
                <img src={selectedProduct.image_url} alt="Product" className="w-48 h-48 object-contain mb-4" />
                <div className="bg-green-50 text-green-800 border border-green-200 text-xs px-3 py-1 rounded w-full text-center">
                  <span className="font-bold">Verified Purchase</span> History
                </div>
              </div>
              
              {/* Content side */}
              <div className="w-full md:w-2/3">
                <h2 className="text-xl font-medium text-black leading-tight mb-2">
                  {selectedProduct.name} (Pre-Owned)
                </h2>
                
                <div className="flex items-center space-x-4 mb-4 text-sm">
                  <span className="bg-[#232F3E] text-white px-2 py-0.5 rounded-sm font-bold text-xs">Second Life</span>
                  <span className="text-[#007185]">Visit the Pre-Owned Store</span>
                </div>
                
                <div className="mb-4">
                  <div className="text-3xl text-[#B12704] font-medium">₹{priceData.final_price_to_buyer_low}</div>
                  <div className="text-sm text-gray-500">
                    Inclusive of all taxes & delivery to {priceData.breakdown.delivery_zone}
                  </div>
                </div>
                
                <div className="border-t border-b border-gray-200 py-3 mb-4 text-sm">
                  <div className="flex mb-2">
                    <span className="w-32 text-gray-600 font-bold">Condition:</span>
                    <span className="font-bold text-black">Used - Working Condition</span>
                  </div>
                  <div className="flex mb-2">
                    <span className="w-32 text-gray-600 font-bold">Verification:</span>
                    <span className="text-gray-800">Physical check at pickup</span>
                  </div>
                  <div className="flex">
                    <span className="w-32 text-gray-600 font-bold">Seller Policy:</span>
                    <span className="text-gray-800">No Return. Penalty for misrepresentation.</span>
                  </div>
                </div>
                
                <ul className="list-disc pl-5 text-sm space-y-1 text-black">
                  <li>Seller assures product is fully functional.</li>
                  <li>Physical verification will be done by delivery executive at the time of pickup.</li>
                  <li>In case of defect, order will be cancelled instantly.</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="mt-8 bg-blue-50 border border-blue-200 p-4 rounded text-sm text-blue-800">
            <strong>Important:</strong> The product stays with you until a buyer orders it. There is zero storage cost. When an order is placed, an Amazon executive will visit your home to verify the condition before pickup.
          </div>

          <div className="mt-6 flex justify-between items-center pt-4 border-t border-gray-200">
            <button onClick={() => setStep(2)} className="text-[#007185] hover:underline font-bold">
              &lsaquo; Edit Terms
            </button>
            <button 
              onClick={confirmListing} 
              className="btn-yellow px-8 py-3 text-base font-bold"
              disabled={submitMutation.isPending}
            >
              {submitMutation.isPending ? "Listing..." : "Confirm & List on Amazon"}
            </button>
          </div>
        </div>
      )}

      {/* Step 4: Success */}
      {step === 4 && listingData && (
        <div className="bg-white p-8 border border-gray-200 rounded-sm text-center max-w-2xl mx-auto shadow-sm">
          <div className="flex justify-center mb-6">
            <CheckCircle className="text-green-600" size={64} />
          </div>
          <h1 className="text-3xl font-bold mb-2">Listing Successful!</h1>
          <p className="text-gray-600 mb-8">{listingData.message}</p>
          
          <div className="bg-gray-50 border border-gray-200 p-6 rounded-lg text-left mb-8">
            <h3 className="font-bold text-lg mb-4">What happens next?</h3>
            
            <div className="space-y-4">
              <div className="flex items-start">
                <div className="bg-white p-2 rounded-full border border-gray-300 mr-4 shadow-sm">
                  <MapPin size={20} className="text-[#007185]" />
                </div>
                <div>
                  <h4 className="font-bold text-sm">1. Item stays at home</h4>
                  <p className="text-sm text-gray-600 mt-1">Keep using or storing your item safely. We bear zero storage cost, and you don't need to ship anything yet.</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="bg-white p-2 rounded-full border border-gray-300 mr-4 shadow-sm">
                  <CheckCircle size={20} className="text-[#007185]" />
                </div>
                <div>
                  <h4 className="font-bold text-sm">2. Verification at Pickup</h4>
                  <p className="text-sm text-gray-600 mt-1">When an order is placed, our executive visits to verify the product works. (Penalty applies if misrepresented).</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="bg-white p-2 rounded-full border border-gray-300 mr-4 shadow-sm">
                  <IndianRupee size={20} className="text-[#007185]" />
                </div>
                <div>
                  <h4 className="font-bold text-sm">3. Get Paid</h4>
                  <p className="text-sm text-gray-600 mt-1">Receive ₹{priceData.seller_receives} directly to your Amazon Pay wallet upon successful delivery to the buyer.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-center space-x-4">
            <Link to="/" className="btn-secondary px-6">Return Home</Link>
            <Link to="/seller" className="btn-yellow px-6 shadow-sm">Go to Dashboard</Link>
          </div>
        </div>
      )}

    </div>
  );
};

export default SellFlow;
