import React from 'react';
import { Bot } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { AIModel } from '../../types/chat.types';

interface ModelSelectorProps {
  selectedModel: AIModel;
  onSelectModel: (model: AIModel) => void;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({ selectedModel, onSelectModel }) => {
  const { t } = useLanguage();

  const models: { value: AIModel; label: string }[] = [
    { value: 'Gemini', label: t('chat.model.gemini') },
    { value: 'GPT', label: t('chat.model.gpt') },
    { value: 'DEEPSEEK', label: t('chat.model.deepseek') },
  ];

  return (
    <div className="flex items-center gap-2">
      <Bot className="w-5 h-5 text-gray-600" />
      <select
        value={selectedModel}
        onChange={(e) => onSelectModel(e.target.value as AIModel)}
        className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
      >
        {models.map((model) => (
          <option key={model.value} value={model.value}>
            {model.label}
          </option>
        ))}
      </select>
    </div>
  );
};