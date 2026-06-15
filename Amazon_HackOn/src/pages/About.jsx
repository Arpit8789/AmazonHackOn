import { Server, Database, BrainCircuit, Cpu, Layout, Globe, Lock, ShieldCheck } from 'lucide-react';

const About = () => {
  return (
    <div className="max-w-6xl mx-auto w-full">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold mb-4">Second Life Commerce — Hackathon Prototype</h1>
        <p className="text-gray-600 max-w-3xl mx-auto">
          A fully integrated AI-powered system handling customer returns, P2P resale, and seller workflows. 
          Built with React, FastAPI, and live Machine Learning models.
        </p>
      </div>

      {/* Tech Stack */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div className="amazon-card shadow-sm border-t-4 border-t-[#FF9900]">
          <h2 className="text-xl font-bold mb-4 flex items-center">
            <Layout className="text-[#007185] mr-2" />
            Frontend Architecture
          </h2>
          <ul className="space-y-4">
            <li className="flex items-start">
              <span className="bg-blue-100 text-blue-800 font-bold px-2 py-1 rounded text-xs mr-3 mt-0.5">React 18</span>
              <div>
                <p className="font-bold text-sm">Vite + React Query</p>
                <p className="text-xs text-gray-600">Fast local dev server, robust data fetching, and optimistic UI updates.</p>
              </div>
            </li>
            <li className="flex items-start">
              <span className="bg-teal-100 text-teal-800 font-bold px-2 py-1 rounded text-xs mr-3 mt-0.5">Tailwind</span>
              <div>
                <p className="font-bold text-sm">Utility-First CSS</p>
                <p className="text-xs text-gray-600">Custom Amazon India design tokens, responsive layouts, exact color matching.</p>
              </div>
            </li>
            <li className="flex items-start">
              <span className="bg-gray-100 text-gray-800 font-bold px-2 py-1 rounded text-xs mr-3 mt-0.5">Router</span>
              <div>
                <p className="font-bold text-sm">React Router v6</p>
                <p className="text-xs text-gray-600">Client-side routing across 5 distinct user flows.</p>
              </div>
            </li>
          </ul>
        </div>

        <div className="amazon-card shadow-sm border-t-4 border-t-[#007185]">
          <h2 className="text-xl font-bold mb-4 flex items-center">
            <Server className="text-[#FF9900] mr-2" />
            Backend & AI Pipeline
          </h2>
          <ul className="space-y-4">
            <li className="flex items-start">
              <span className="bg-green-100 text-green-800 font-bold px-2 py-1 rounded text-xs mr-3 mt-0.5">FastAPI</span>
              <div>
                <p className="font-bold text-sm">Python Async Backend</p>
                <p className="text-xs text-gray-600">High-performance API handling image uploads and ML inference.</p>
              </div>
            </li>
            <li className="flex items-start">
              <span className="bg-purple-100 text-purple-800 font-bold px-2 py-1 rounded text-xs mr-3 mt-0.5">CLIP</span>
              <div>
                <p className="font-bold text-sm">Zero-Shot Vision Grading</p>
                <p className="text-xs text-gray-600">OpenAI ViT-B/32 analyzing product photos to determine A/B/C condition.</p>
              </div>
            </li>
            <li className="flex items-start">
              <span className="bg-amber-100 text-amber-800 font-bold px-2 py-1 rounded text-xs mr-3 mt-0.5">XGBoost</span>
              <div>
                <p className="font-bold text-sm">Pricing + SHAP Explainer</p>
                <p className="text-xs text-gray-600">Regressive pricing model based on warranty/demand, with transparent SHAP feature importance.</p>
              </div>
            </li>
            <li className="flex items-start">
              <span className="bg-pink-100 text-pink-800 font-bold px-2 py-1 rounded text-xs mr-3 mt-0.5">NLP</span>
              <div>
                <p className="font-bold text-sm">Multilingual MiniLM</p>
                <p className="text-xs text-gray-600">Sentence Transformers executing semantic search over Hindi/English reviews.</p>
              </div>
            </li>
          </ul>
        </div>
      </div>

      {/* Real vs Mock Breakdown */}
      <div className="amazon-card border border-gray-200 p-8 shadow-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">What's Real vs Mock in This Demo?</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
          <div>
            <h3 className="font-bold text-[#007185] border-b border-gray-200 pb-2 mb-4">🟢 Real Components</h3>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start">
                <CheckCircle size={16} className="text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                <span><strong>Vision Grading:</strong> Real PyTorch model (CLIP) running inference on your uploaded photos.</span>
              </li>
              <li className="flex items-start">
                <CheckCircle size={16} className="text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                <span><strong>Pricing Math:</strong> XGBoost actually calculates prices based on the inputs provided.</span>
              </li>
              <li className="flex items-start">
                <CheckCircle size={16} className="text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                <span><strong>Review NLP:</strong> Cosine similarity search running over actual embedded multilingual text.</span>
              </li>
              <li className="flex items-start">
                <CheckCircle size={16} className="text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                <span><strong>Routing Logic:</strong> Pincode-to-demand mapping directly affects the warehouse vs local routing.</span>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-bold text-amazon-orange border-b border-gray-200 pb-2 mb-4">🟠 Mock / Simulated Components</h3>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start">
                <Cpu size={16} className="text-amazon-orange mr-2 mt-0.5 flex-shrink-0" />
                <span><strong>Databases:</strong> Using in-memory Python dictionaries instead of PostgreSQL.</span>
              </li>
              <li className="flex items-start">
                <Cpu size={16} className="text-amazon-orange mr-2 mt-0.5 flex-shrink-0" />
                <span><strong>Order History:</strong> Hardcoded to 6 sample products (Electronics, Baby, Apparel).</span>
              </li>
              <li className="flex items-start">
                <Cpu size={16} className="text-amazon-orange mr-2 mt-0.5 flex-shrink-0" />
                <span><strong>Listing Text:</strong> High-quality templates instead of 7B LLM (to prevent out-of-memory crashes on demo laptops).</span>
              </li>
              <li className="flex items-start">
                <Cpu size={16} className="text-amazon-orange mr-2 mt-0.5 flex-shrink-0" />
                <span><strong>Processing Delays:</strong> Added artificial `setTimeout` to make API calls feel more realistic.</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
