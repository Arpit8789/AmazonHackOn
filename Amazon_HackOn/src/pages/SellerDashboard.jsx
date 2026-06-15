import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Camera, CheckCircle, Activity, Box, IndianRupee, FileText, BarChart3, Clock, AlertTriangle, PlayCircle } from 'lucide-react';
import { apiService } from '../api/api';

const SellerDashboard = () => {
  const [photos, setPhotos] = useState([null, null, null]);
  const [files, setFiles] = useState([null, null, null]);
  const [productData, setProductData] = useState({ name: 'Anker 7-in-1 USB-C Hub', category: 'Electronics', price: 2499, weight: 0.15 });
  const [processingState, setProcessingState] = useState('idle'); // idle, processing, done
  const [result, setResult] = useState(null);

  const autolistMutation = useMutation({
    mutationFn: apiService.sellerAutolist,
    onSuccess: (data) => {
      setResult(data);
      setProcessingState('done');
    }
  });

  const handlePhotoUpload = (index, e) => {
    const file = e.target.files[0];
    if (file) {
      const newPhotos = [...photos];
      newPhotos[index] = URL.createObjectURL(file);
      setPhotos(newPhotos);
      
      const newFiles = [...files];
      newFiles[index] = file;
      setFiles(newFiles);
    }
  };

  const handleProcess = () => {
    if (files.filter(p => p !== null).length < 2) {
      alert("Please upload at least 2 photos for AI processing.");
      return;
    }
    
    setProcessingState('processing');
    
    const formData = new FormData();
    formData.append("product_name", productData.name);
    formData.append("category", productData.category);
    formData.append("original_price", productData.price);
    formData.append("weight_kg", productData.weight);
    
    // Append actual image files
    files.forEach(file => {
      if (file) formData.append("images", file);
    });
    
    autolistMutation.mutate(formData);
  };

  const handlePublish = () => {
    alert("Listing published successfully! It is now live on Amazon Second Life.");
    // Reset
    setProcessingState('idle');
    setResult(null);
    setPhotos([null, null, null]);
  };

  return (
    <div className="max-w-7xl mx-auto w-full">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-gray-200 pb-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold">Seller Returns Hub</h1>
          <p className="text-sm text-gray-600">Automate grading, pricing, and relisting of customer returns in seconds.</p>
        </div>
        
        <div className="mt-4 md:mt-0 flex space-x-4 text-sm">
          <div className="bg-white border border-gray-300 p-2 rounded shadow-sm text-center">
            <div className="text-xs text-gray-500 font-bold uppercase">Time Saved MTD</div>
            <div className="text-xl font-bold text-green-700">42 Hours</div>
          </div>
          <div className="bg-white border border-gray-300 p-2 rounded shadow-sm text-center">
            <div className="text-xs text-gray-500 font-bold uppercase">Auto-Listed MTD</div>
            <div className="text-xl font-bold text-[#007185]">108 Items</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* LEFT COLUMN: Input & Processing */}
        <div className="lg:col-span-1 space-y-6">
          <div className="amazon-card shadow-md border-t-4 border-t-[#FF9900]">
            <h2 className="text-lg font-bold mb-4 flex items-center">
              <PlayCircle className="text-[#007185] mr-2" size={20} />
              New Return Processing
            </h2>
            
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-xs font-bold text-gray-700 mb-1">Product Details</label>
                <input 
                  type="text" 
                  className="amazon-input w-full mb-2" 
                  value={productData.name} 
                  onChange={(e) => setProductData({...productData, name: e.target.value})}
                  placeholder="Product Name"
                />
                <div className="flex space-x-2">
                  <select 
                    className="amazon-input w-1/2"
                    value={productData.category}
                    onChange={(e) => setProductData({...productData, category: e.target.value})}
                  >
                    <option value="Electronics">Electronics</option>
                    <option value="Apparel">Apparel</option>
                    <option value="Home Goods">Home Goods</option>
                  </select>
                  <input 
                    type="number" 
                    className="amazon-input w-1/2" 
                    value={productData.price} 
                    onChange={(e) => setProductData({...productData, price: Number(e.target.value)})}
                    placeholder="Price (₹)"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-gray-700 mb-2">Upload Return Photos (Min 2)</label>
                <div className="flex space-x-2">
                  {[0, 1, 2].map((idx) => (
                    <div key={idx} className="relative w-1/3 aspect-square border-2 border-dashed border-gray-300 bg-gray-50 rounded flex items-center justify-center overflow-hidden">
                      {photos[idx] ? (
                        <img src={photos[idx]} alt="Return" className="w-full h-full object-cover" />
                      ) : (
                        <Camera size={20} className="text-gray-400" />
                      )}
                      <input 
                        type="file" 
                        accept="image/*" 
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        onChange={(e) => handlePhotoUpload(idx, e)}
                        disabled={processingState !== 'idle'}
                      />
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <button 
              onClick={handleProcess} 
              className="btn-yellow w-full py-3 font-bold shadow-md"
              disabled={processingState !== 'idle'}
            >
              {processingState === 'idle' ? "Process Return with AI" : "Processing..."}
            </button>
          </div>

          {/* Processing Animation */}
          {processingState === 'processing' && (
            <div className="amazon-card border-[#007185] bg-[#F0F8FF]">
              <h3 className="font-bold text-[#007185] mb-4 flex items-center">
                <Activity className="animate-pulse mr-2" size={18} />
                AI is analyzing...
              </h3>
              
              <div className="space-y-4">
                <div className="flex items-center text-sm">
                  <div className="w-5 h-5 rounded-full border-2 border-[#007185] border-t-transparent animate-spin mr-3"></div>
                  <span className="text-gray-700">Vision grading product condition (CLIP)</span>
                </div>
                <div className="flex items-center text-sm opacity-50">
                  <div className="w-5 h-5 rounded-full border-2 border-gray-400 border-t-transparent mr-3"></div>
                  <span className="text-gray-500">Calculating resale price (XGBoost)</span>
                </div>
                <div className="flex items-center text-sm opacity-50">
                  <div className="w-5 h-5 rounded-full border-2 border-gray-400 border-t-transparent mr-3"></div>
                  <span className="text-gray-500">Generating SEO listing tags</span>
                </div>
              </div>
            </div>
          )}

          {/* Business Impact Box */}
          <div className="border border-gray-200 rounded p-4 bg-gray-50">
            <h3 className="font-bold text-sm mb-2">Traditional Process</h3>
            <div className="flex justify-between items-center text-sm mb-1">
              <span className="text-gray-600">Manual inspection</span>
              <span>10 mins</span>
            </div>
            <div className="flex justify-between items-center text-sm mb-1">
              <span className="text-gray-600">Pricing research</span>
              <span>10 mins</span>
            </div>
            <div className="flex justify-between items-center text-sm mb-3">
              <span className="text-gray-600">Listing creation</span>
              <span>5 mins</span>
            </div>
            <div className="flex justify-between items-center font-bold text-red-600 border-t border-gray-200 pt-2">
              <span>Total Time:</span>
              <span>25 minutes</span>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: Results */}
        <div className="lg:col-span-2">
          {processingState === 'idle' && !result && (
            <div className="h-full flex flex-col items-center justify-center text-gray-400 border-2 border-dashed border-gray-300 rounded-lg p-10 bg-gray-50">
              <Box size={64} className="mb-4 opacity-50" />
              <h2 className="text-xl font-bold text-gray-500">Awaiting Product</h2>
              <p className="text-center mt-2 text-sm max-w-sm">
                Upload photos of a returned item on the left to automatically generate its grade, optimal price, and complete Amazon listing in seconds.
              </p>
            </div>
          )}

          {result && processingState === 'done' && (
            <div className="space-y-6">
              
              <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded shadow-sm flex items-center justify-between">
                <div className="flex items-center font-bold">
                  <CheckCircle className="mr-2" />
                  Processed successfully in {result.processing_time_seconds || 1.4} seconds
                </div>
                <div className="text-sm font-medium">
                  Saved: {result.time_saved_minutes || 25} minutes
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Grading Result */}
                <div className="amazon-card shadow-sm border-t-4 border-t-blue-500">
                  <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4 flex items-center">
                    <Camera size={14} className="mr-1" /> AI Vision Grading
                  </h3>
                  
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <div className="text-3xl font-black text-blue-600">Grade {result.grade.grade}</div>
                      <div className="text-sm text-gray-500">Condition Rating</div>
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 p-3 rounded border border-gray-200 text-sm">
                    <strong>Defect Analysis:</strong> {result.grade.defects_description}
                  </div>
                </div>

                {/* Pricing Result */}
                <div className="amazon-card shadow-sm border-t-4 border-t-green-500">
                  <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4 flex items-center">
                    <IndianRupee size={14} className="mr-1" /> ML Pricing Recommendation
                  </h3>
                  
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <div className="text-3xl font-black text-green-600">₹{result.price.price_high}</div>
                      <div className="text-sm text-gray-500">Optimal Resale Price</div>
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 p-3 rounded border border-gray-200 text-sm">
                    <strong>Why this price?</strong> Based on {result.price.shap_explanation?.[0]?.factor || "warranty remaining"} and current market demand.
                  </div>
                </div>
              </div>

              {/* Generated Listing */}
              <div className="amazon-card shadow-sm border-t-4 border-t-purple-500">
                <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4 flex items-center justify-between">
                  <span className="flex items-center"><FileText size={14} className="mr-1" /> Generated Listing Content</span>
                  <span className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded-full text-xs">SEO Score: {result.listing.seo_score}/100</span>
                </h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-bold text-gray-700 mb-1">Listing Title</label>
                    <input 
                      type="text" 
                      className="amazon-input w-full font-medium" 
                      defaultValue={result.listing.title}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-xs font-bold text-gray-700 mb-1">Product Description</label>
                    <textarea 
                      className="amazon-input w-full h-32 text-sm leading-relaxed" 
                      defaultValue={result.listing.description}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-xs font-bold text-gray-700 mb-1">Generated Meta Tags</label>
                    <div className="flex flex-wrap gap-2">
                      {result.listing.meta_tags.map(tag => (
                        <span key={tag} className="bg-gray-100 border border-gray-300 text-gray-700 px-2 py-1 rounded text-xs">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mt-6 border-t border-gray-200 pt-4 flex justify-end">
                  <button onClick={handlePublish} className="btn-yellow px-8 py-2.5 font-bold shadow-sm text-base">
                    Publish to Second Life Store
                  </button>
                </div>
              </div>

            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default SellerDashboard;
