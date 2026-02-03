import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  className?: string;
}

const sizeMap = {
  sm: 'w-8 h-8',
  md: 'w-16 h-16',
  lg: 'w-24 h-24',
};

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  text = '로딩 중...',
  className = '',
}) => {
  return (
    <div className={`flex flex-col items-center justify-center gap-4 ${className}`}>
      <img
        src="/images/loading-spinner.svg"
        alt="로딩 중"
        className={`${sizeMap[size]} animate-spin`}
      />
      {text && (
        <p className="text-gray-500 text-sm font-medium">{text}</p>
      )}
    </div>
  );
};

export default LoadingSpinner;
