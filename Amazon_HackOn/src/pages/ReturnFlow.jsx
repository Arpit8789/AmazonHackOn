import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Camera, ChevronRight, CheckCircle, AlertTriangle, Package, MapPin, Truck, Leaf, Clock } from 'lucide-react';
import { apiService } from '../api/api';

const ReturnFlow = ({ preSelectedOrder = null, onComplete = null }) => {
  const [step, setStep] = useState(preSelectedOrder ? 2 : 1);
  const [selectedProduct, setSelectedProduct] = useState(preSelectedOrder);
  const [returnReason, setReturnReason] = useState("");
  const [initiateData, setInitiateData] = useState(preSelectedOrder ? {
    instructions: "Try to upload 3 to 4 images from all dimensions for getting correct resale and return evaluation.",
    angle_guide: ["Image 1", "Image 2", "Image 3", "Image 4 (Optional)"]
  } : null);
  const [uploadedPhotos, setUploadedPhotos] = useState({});
  const [gradeResult, setGradeResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // 1. Fetch products
  const { data: products, isLoading: loadingProducts } = useQuery({
    queryKey: ['demo-products'],
    queryFn: apiService.getProducts,
  });

  // 2. Initiate return mutation
  const initiateMutation = useMutation({
    mutationFn: apiService.initiateReturn,
    onSuccess: (data) => {
      setInitiateData(data);
      setStep(2);
    }
  });

  // 3. Grade product mutation
  const gradeMutation = useMutation({
    mutationFn: apiService.gradeProduct,
    onSuccess: (data) => {
      setGradeResult(data);
      setIsProcessing(false);
      setStep(3);
    }
  });

  const handleInitiate = (product) => {
    if (!returnReason) {
      alert("Please select a return reason");
      return;
    }
    setSelectedProduct(product);
    initiateMutation.mutate({
      order_id: product.order_id,
      product_name: product.name,
      product_category: product.category,
      return_reason: returnReason,
      pincode: "110001", // Demo value
      original_price: product.original_price
    });
  };

  const [uploadedFiles, setUploadedFiles] = useState({});

  const handlePhotoUpload = (angle, e) => {
    const file = e.target.files[0];
    if (file) {
      // Create local preview URL
      const previewUrl = URL.createObjectURL(file);
      setUploadedPhotos(prev => ({ ...prev, [angle]: previewUrl }));
      setUploadedFiles(prev => ({ ...prev, [angle]: file }));
    }
  };

  const submitForGrading = () => {
    const angles = initiateData.angle_guide;
    if (Object.keys(uploadedPhotos).length < angles.length) {
      alert("Please upload all required photos");
      return;
    }
    
    setIsProcessing(true);
    
    const formData = new FormData();
    formData.append("return_reason", returnReason);
    formData.append("product_category", selectedProduct.category);
    formData.append("original_price", selectedProduct.original_price);
    formData.append("pincode", "110001");
    formData.append("product_name", selectedProduct.name);
    formData.append("image_url", selectedProduct.image_url);
    
    // Append actual image files
    Object.values(uploadedFiles).forEach(file => {
      formData.append("images", file);
    });
    
    gradeMutation.mutate(formData);
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Breadcrumbs / Progress */}
      <div className="flex items-center text-sm text-gray-500 mb-6">
        <span className={step >= 1 ? "font-bold text-black" : ""}>Your Orders</span>
        <ChevronRight size={16} className="mx-2" />
        <span className={step >= 2 ? "font-bold text-black" : ""}>Upload Photos</span>
        <ChevronRight size={16} className="mx-2" />
        <span className={step >= 3 ? "font-bold text-black" : ""}>Processing</span>
        <ChevronRight size={16} className="mx-2" />
        <span className={step >= 4 ? "font-bold text-black" : ""}>Confirmation</span>
      </div>

      {/* Step 1: Select Order */}
      {step === 1 && (
        <div className="bg-white p-6 border border-gray-200 rounded-2xl">
          <h1 className="text-2xl font-bold mb-6">Choose items to return</h1>
          
          {loadingProducts ? (
            <p>Loading your orders...</p>
          ) : (
            <div className="space-y-6">
              {products?.slice(0, 2).map((product) => (
                <div key={product.product_id} className="border border-gray-200 p-4 rounded flex flex-col md:flex-row gap-4">
                  <div className="w-32 h-32 flex-shrink-0 bg-gray-100 p-2">
                    <img src={product.image_url} alt={product.name} className="w-full h-full object-contain" />
                  </div>
                  <div className="flex-grow">
                    <h3 className="font-bold text-lg text-[#007185] cursor-pointer hover:text-[#C45500] hover:underline">
                      {product.name}
                    </h3>
                    <p className="text-sm text-gray-600 mb-1">Delivered {product.purchase_date}</p>
                    <p className="font-bold">₹{product.original_price}</p>
                    
                    <div className="mt-4">
                      <label className="block text-sm font-bold mb-1">Please provide the exact reason for return</label>
                      <textarea 
                        className="amazon-input w-full md:w-3/4 p-3 shadow-inner resize-none"
                        rows="3"
                        placeholder="Give a proper reason for return so we can process it accurately..."
                        onChange={(e) => setReturnReason(e.target.value)}
                        value={returnReason}
                      ></textarea>
                    </div>
                  </div>
                  <div className="flex flex-col justify-center min-w-[150px]">
                    <button 
                      onClick={() => handleInitiate(product)}
                      className="btn-yellow w-full py-1.5"
                      disabled={initiateMutation.isPending}
                    >
                      Return Item
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Step 2: Photo Upload */}
      {step === 2 && initiateData && (
        <div className="bg-white p-6 border border-gray-200 rounded-2xl">
          <h1 className="text-2xl font-bold mb-2">Upload Photos for Return</h1>
          <p className="text-gray-600 mb-6">{initiateData.instructions}</p>
          

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            {initiateData.angle_guide.map((angle, index) => (
              <div key={index} className="border-2 border-dashed border-gray-300 rounded-xl p-4 flex flex-col items-center justify-center h-48 bg-gray-50 relative overflow-hidden group">
                {uploadedPhotos[angle] ? (
                  <>
                    <img src={uploadedPhotos[angle]} alt={angle} className="absolute inset-0 w-full h-full object-cover" />
                    <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <span className="text-white font-bold text-sm bg-black px-2 py-1 rounded">Change Photo</span>
                    </div>
                  </>
                ) : (
                  <>
                    <Camera size={32} className="text-gray-400 mb-2" />
                    <span className="font-bold text-sm text-center">{angle}</span>
                    <span className="text-xs text-gray-500 mt-1">Tap to upload</span>
                  </>
                )}
                <input 
                  type="file" 
                  accept="image/*" 
                  capture="environment"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  onChange={(e) => handlePhotoUpload(angle, e)}
                />
              </div>
            ))}
          </div>

          <div className="flex justify-between items-center border-t border-gray-200 pt-4">
            <button onClick={() => setStep(1)} className="px-4 py-2 text-sm text-blue-600 hover:underline">
              Back
            </button>
            <button 
              onClick={submitForGrading}
              className="btn-yellow px-8 py-2 relative"
              disabled={isProcessing}
            >
              {isProcessing ? "Processing Return..." : "Submit Return"}
            </button>
          </div>
        </div>
      )}

      {/* Processing Overlay */}
      {isProcessing && (
        <div className="fixed inset-0 bg-black bg-opacity-70 z-50 flex flex-col items-center justify-center text-white">
          <div className="w-20 h-20 border-4 border-[#FF9900] border-t-transparent rounded-full animate-spin mb-6"></div>
          <h2 className="text-2xl font-bold mb-2">Processing Return</h2>
          <p className="text-gray-300">Verifying return details and photos...</p>
        </div>
      )}

      {/* Step 3: Return Underway — User sees friendly confirmation, grade is used by backend */}
      {step === 3 && (
        <div className="bg-white p-8 border border-gray-200 rounded-2xl text-center">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
              <CheckCircle className="text-green-600" size={40} />
            </div>
          </div>
          <h1 className="text-3xl font-bold mb-4">Return is Underway</h1>
          <p className="text-lg text-gray-600 mb-4 max-w-xl mx-auto">
            Your return request for <strong>{selectedProduct?.name || selectedProduct?.product_name}</strong> has been successfully submitted.
          </p>
          <p className="text-base text-gray-500 mb-8 max-w-xl mx-auto">
            Your refund of <strong>₹{selectedProduct?.original_price}</strong> will be processed to your original payment method once the pickup is complete.
          </p>
          
          <div className="bg-gray-50 border border-gray-200 p-6 rounded-xl max-w-md mx-auto mb-8 text-left">
            <h3 className="font-bold mb-3 flex items-center"><Clock size={16} className="mr-2 text-[#007185]" />Next Steps</h3>
            <ul className="text-sm space-y-3">
              <li className="flex items-start">
                <span className="font-bold mr-2 text-gray-400">1.</span>
                <span>Keep the item ready in its original packaging.</span>
              </li>
              <li className="flex items-start">
                <span className="font-bold mr-2 text-gray-400">2.</span>
                <span>Pickup scheduled for tomorrow between 9 AM - 7 PM.</span>
              </li>
              <li className="flex items-start">
                <span className="font-bold mr-2 text-gray-400">3.</span>
                <span>Ensure the item matches the exact condition shown in your uploaded photos at the time of pickup.</span>
              </li>
            </ul>
          </div>


          {onComplete ? (
            <button onClick={onComplete} className="bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-xl px-8 py-2 text-[14px] shadow-sm font-medium">
              Close Window
            </button>
          ) : (
            <Link to="/" className="bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-xl px-8 py-2 text-[14px] shadow-sm font-medium">
              Return to Homepage
            </Link>
          )}
        </div>
      )}

    </div>
  );
};

export default ReturnFlow;
