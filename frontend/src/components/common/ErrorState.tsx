import React from 'react';

interface ErrorStateProps {
    title?: string;
    message?: string;
    onRetry?: () => void;
    className?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
    title = '문제가 발생했습니다',
    message = '잠시 후 다시 시도해 주세요.',
    onRetry,
    className = '',
}) => {
    return (
        <div className={`flex flex-col items-center justify-center gap-6 p-8 ${className}`}>
            <img
                src="/images/error.png"
                alt="에러 발생"
                className="w-48 h-48 object-contain"
            />
            <div className="text-center">
                <h3 className="text-xl font-bold text-gray-800 mb-2">{title}</h3>
                <p className="text-gray-500">{message}</p>
            </div>
            {onRetry && (
                <button
                    onClick={onRetry}
                    className="px-6 py-2 bg-emerald-500 text-white rounded-lg font-medium 
                     hover:bg-emerald-600 transition-colors focus:outline-none focus:ring-2 
                     focus:ring-emerald-500 focus:ring-offset-2"
                >
                    다시 시도
                </button>
            )}
        </div>
    );
};

export default ErrorState;
