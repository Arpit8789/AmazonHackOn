import { X } from 'lucide-react';
import ReturnFlow from '../pages/ReturnFlow';

export default function ReturnPopup({ order, onClose }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4">
      <div className="bg-[#EAEDED] rounded-lg max-w-5xl w-full shadow-2xl overflow-hidden flex flex-col max-h-[95vh]">
        
        {/* Header */}
        <div className="bg-white border-b border-gray-300 px-6 py-4 flex justify-between items-center">
          <h2 className="text-xl font-bold">Return Item</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-black">
            <X size={24} />
          </button>
        </div>

        {/* Content - Embeds the ReturnFlow but we'll pass the order to skip step 1 */}
        <div className="p-6 overflow-y-auto bg-white m-4 rounded shadow-sm">
          <ReturnFlow preSelectedOrder={order} onComplete={onClose} />
        </div>

      </div>
    </div>
  );
}
