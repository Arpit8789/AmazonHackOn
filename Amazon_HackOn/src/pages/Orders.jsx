import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../api/api';
import { Search, ChevronDown } from 'lucide-react';
import ResalePopup from '../components/ResalePopup';
import ReturnPopup from '../components/ReturnPopup';

export default function Orders() {
  const [activeTab, setActiveTab] = useState('orders');
  const [resaleItem, setResaleItem] = useState(null);
  const [returnItem, setReturnItem] = useState(null);

  const { data, isLoading } = useQuery({
    queryKey: ['my-orders'],
    queryFn: async () => {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
      const res = await fetch(`${apiUrl}/orders/me`);
      if (!res.ok) throw new Error('Network response was not ok');
      const json = await res.json();
      return json.data;
    }
  });

  return (
    <div className="max-w-5xl mx-auto px-4 py-6 font-sans">
      
      {/* Breadcrumbs */}
      <div className="text-sm text-gray-500 mb-4">
        Your Account › <span className="text-[#c45500] font-bold">Your Orders</span>
      </div>

      <div className="flex justify-between items-end mb-4">
        <h1 className="text-3xl font-normal">Your Orders</h1>
        <div className="flex items-center w-full max-w-md ml-4">
          <div className="relative w-full flex">
            <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-500">
              <Search size={18} />
            </span>
            <input 
              type="text" 
              className="w-full border border-gray-400 rounded-l shadow-inner py-1.5 pl-10 pr-3 focus:outline-none focus:border-[#007185] focus:ring-1 focus:ring-[#007185]"
              placeholder="Search all orders"
            />
            <button className="bg-[#333333] hover:bg-[#222222] text-white px-4 py-1.5 rounded-r border border-[#333333]">
              Search Orders
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 mb-6 space-x-6 text-sm">
        <button className={`pb-2 ${activeTab === 'orders' ? 'font-bold text-[#c45500] border-b-2 border-[#c45500]' : 'text-[#007185] hover:text-[#c45500] hover:underline'}`} onClick={() => setActiveTab('orders')}>Orders</button>
        <button className={`pb-2 ${activeTab === 'buy-again' ? 'font-bold text-[#c45500] border-b-2 border-[#c45500]' : 'text-[#007185] hover:text-[#c45500] hover:underline'}`} onClick={() => setActiveTab('buy-again')}>Buy Again</button>
        <button className={`pb-2 ${activeTab === 'not-dispatched' ? 'font-bold text-[#c45500] border-b-2 border-[#c45500]' : 'text-[#007185] hover:text-[#c45500] hover:underline'}`} onClick={() => setActiveTab('not-dispatched')}>Not Yet Dispatched</button>
        <button className={`pb-2 ${activeTab === 'cancelled' ? 'font-bold text-[#c45500] border-b-2 border-[#c45500]' : 'text-[#007185] hover:text-[#c45500] hover:underline'}`} onClick={() => setActiveTab('cancelled')}>Cancelled Orders</button>
      </div>

      {/* Filter */}
      <div className="flex items-center mb-4 text-sm">
        <span className="font-bold mr-2">12 orders</span>
        <span className="mr-2">placed in</span>
        <select className="border border-gray-300 rounded p-1 bg-[#F0F2F2] shadow-sm hover:bg-[#e3e6e6] cursor-pointer">
          <option>past 6 months</option>
          <option>2026</option>
          <option>2025</option>
        </select>
      </div>

      {/* Orders List */}
      <div className="space-y-6">
        {isLoading ? (
          <div className="py-10 text-center">Loading orders...</div>
        ) : data?.length === 0 ? (
          <div className="py-10 text-center text-gray-500">No orders found.</div>
        ) : (
          data?.map((order) => (
            <div key={order.order_id} className="border border-[#D5D9D9] rounded-lg overflow-hidden bg-white shadow-sm mb-4">
              {/* Order Header */}
              <div className="bg-[#F0F2F2] border-b border-[#D5D9D9] p-4 flex justify-between text-sm text-[#565959]">
                <div className="flex space-x-8">
                  <div>
                    <div className="uppercase text-xs font-bold mb-0.5">Order Placed</div>
                    <div>{order.purchase_date}</div>
                  </div>
                  <div>
                    <div className="uppercase text-xs font-bold mb-0.5">Total</div>
                    <div>₹{order.original_price}</div>
                  </div>
                  <div>
                    <div className="uppercase text-xs font-bold mb-0.5">Dispatch To</div>
                    <div className="text-[#007185] hover:underline hover:text-[#c45500] cursor-pointer flex items-center">
                      Arpit <ChevronDown size={14} className="ml-0.5" />
                    </div>
                  </div>
                </div>
                <div className="text-right flex flex-col justify-end">
                  <div className="uppercase text-xs font-bold mb-0.5 text-right w-full flex justify-end">Order # {order.order_id}</div>
                  <div className="flex space-x-2 text-[#007185]">
                    <span className="hover:underline cursor-pointer">View order details</span>
                    <span className="text-gray-300">|</span>
                    <span className="hover:underline cursor-pointer">Invoice</span>
                  </div>
                </div>
              </div>

              {/* Order Body */}
              <div className="p-4 flex flex-col md:flex-row gap-6">
                <div className="w-24 h-24 flex-shrink-0">
                  <img src={order.image_url} alt={order.product_name} className="w-full h-full object-contain mix-blend-multiply" />
                </div>
                
                <div className="flex-grow">
                  <h3 className="font-bold text-base text-[#007185] hover:text-[#c45500] hover:underline cursor-pointer line-clamp-2 leading-tight">
                    {order.product_name}
                  </h3>
                  {!order.return_eligible && (
                    <div className="text-sm mt-1 text-gray-500">
                      Return window closed on {order.purchase_date}
                    </div>
                  )}
                  <div className="mt-4 flex space-x-2">
                    <button className="bg-white border border-[#D5D9D9] hover:bg-gray-50 rounded-lg px-3 py-1.5 text-sm shadow-sm flex items-center">
                      Buy it again
                    </button>
                    <button className="bg-white border border-[#D5D9D9] hover:bg-gray-50 rounded-lg px-3 py-1.5 text-sm shadow-sm flex items-center">
                      View your item
                    </button>
                  </div>
                </div>

                {/* Right side Action Buttons (The Second Life Integrations!) */}
                <div className="w-full md:w-56 flex flex-col space-y-2 border-t md:border-t-0 md:border-l border-[#D5D9D9] pt-4 md:pt-0 md:pl-4">
                  <button className="w-full bg-white border border-[#D5D9D9] hover:bg-gray-50 rounded-lg px-3 py-1.5 text-sm shadow-sm text-center">
                    Track package
                  </button>
                  
                  {/* Return Option */}
                  {order.return_eligible && (
                    <button 
                      onClick={() => setReturnItem(order)}
                      className="w-full bg-white border border-[#D5D9D9] hover:bg-gray-50 rounded-lg px-3 py-1.5 text-sm shadow-sm text-center"
                    >
                      Return or replace items
                    </button>
                  )}
                  
                  {/* Resell Option */}
                  {order.resell_eligible && (
                    <button 
                      onClick={() => setResaleItem(order)}
                      className="w-full bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] rounded-lg px-3 py-1.5 text-sm shadow-sm text-center font-medium"
                    >
                      Resell on Second Life
                    </button>
                  )}

                  <button className="w-full bg-white border border-[#D5D9D9] hover:bg-gray-50 rounded-lg px-3 py-1.5 text-sm shadow-sm text-center">
                    Write a product review
                  </button>
                  <button className="w-full bg-white border border-[#D5D9D9] hover:bg-gray-50 rounded-lg px-3 py-1.5 text-sm shadow-sm text-center hidden md:block">
                    Archive order
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {resaleItem && (
        <ResalePopup 
          order={resaleItem} 
          onClose={() => setResaleItem(null)} 
        />
      )}

      {returnItem && (
        <ReturnPopup 
          order={returnItem} 
          onClose={() => setReturnItem(null)} 
        />
      )}

    </div>
  );
}
