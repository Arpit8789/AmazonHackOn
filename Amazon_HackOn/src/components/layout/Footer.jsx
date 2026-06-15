import { Leaf } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="mt-auto">
      {/* Back to top */}
      <div className="bg-[#37475A] hover:bg-[#485769] text-white text-center py-4 text-sm cursor-pointer transition-colors">
        Back to top
      </div>

      {/* Main Footer Links */}
      <div className="bg-amazon-light text-white py-10 px-4 md:px-20">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 max-w-5xl mx-auto">
          <div>
            <h3 className="font-bold mb-4 text-base">Get to Know Us</h3>
            <ul className="space-y-2 text-sm text-[#CCCCCC]">
              <li className="hover:underline cursor-pointer">About Us</li>
              <li className="hover:underline cursor-pointer">Careers</li>
              <li className="hover:underline cursor-pointer">Press Releases</li>
              <li className="hover:underline cursor-pointer">Amazon Science</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold mb-4 text-base">Connect with Us</h3>
            <ul className="space-y-2 text-sm text-[#CCCCCC]">
              <li className="hover:underline cursor-pointer">Facebook</li>
              <li className="hover:underline cursor-pointer">Twitter</li>
              <li className="hover:underline cursor-pointer">Instagram</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold mb-4 text-base">Make Money with Us</h3>
            <ul className="space-y-2 text-sm text-[#CCCCCC]">
              <li className="hover:underline cursor-pointer">Sell on Amazon</li>
              <li className="hover:underline cursor-pointer">Sell under Amazon Accelerator</li>
              <li className="hover:underline cursor-pointer">Protect and Build Your Brand</li>
              <li className="hover:underline cursor-pointer text-amazon-yellow font-medium">Second Life Commerce</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold mb-4 text-base">Let Us Help You</h3>
            <ul className="space-y-2 text-sm text-[#CCCCCC]">
              <li className="hover:underline cursor-pointer">COVID-19 and Amazon</li>
              <li className="hover:underline cursor-pointer">Your Account</li>
              <li className="hover:underline cursor-pointer">Returns Centre</li>
              <li className="hover:underline cursor-pointer">100% Purchase Protection</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Second Life Impact Banner */}
      <div className="bg-amazon border-t border-[#3a4553] py-8 text-center px-4">
        <div className="flex flex-col items-center justify-center max-w-4xl mx-auto">
          <div className="flex items-center space-x-2 text-amazon-yellow font-bold text-xl mb-4">
            <Leaf size={24} />
            <span>Amazon Second Life</span>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-white w-full text-center">
            <div className="flex flex-col">
              <span className="text-2xl font-bold">12.4M</span>
              <span className="text-xs text-[#CCCCCC]">Products Rescued</span>
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-bold">₹8,325 Cr</span>
              <span className="text-xs text-[#CCCCCC]">Seller Value Recovered</span>
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-bold">45,000+</span>
              <span className="text-xs text-[#CCCCCC]">Tons E-Waste Prevented</span>
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-bold">2.1M</span>
              <span className="text-xs text-[#CCCCCC]">P2P Resale Users</span>
            </div>
          </div>
        </div>
        
        <div className="mt-8 pt-6 border-t border-[#3a4553] flex flex-col md:flex-row items-center justify-center space-y-2 md:space-y-0 md:space-x-8 text-xs text-[#CCCCCC]">
          <span className="hover:underline cursor-pointer">Conditions of Use & Sale</span>
          <span className="hover:underline cursor-pointer">Privacy Notice</span>
          <span className="hover:underline cursor-pointer">Interest-Based Ads</span>
          <span>© 1996-2026, Amazon.com, Inc. or its affiliates</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
