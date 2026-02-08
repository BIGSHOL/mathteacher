import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useAuthStore } from '../../store/authStore'
import api from '../../lib/api'
import { Link } from 'react-router-dom'

interface ShopItem {
    id: string
    name: string
    type: string
    description: string
    price: number
    image_url: string
    is_active: boolean
}

export function ShopPage() {
    const { user, fetchUser } = useAuthStore()
    const [items, setItems] = useState<ShopItem[]>([])
    const [loading, setLoading] = useState(true)
    const [purchaseLoading, setPurchaseLoading] = useState<string | null>(null)

    const fetchItems = async () => {
        try {
            const { data } = await api.get('/shop/items')
            setItems(data.data)
        } catch (error) {
            console.error('Failed to fetch shop items:', error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchItems()
    }, [])

    const handlePurchase = async (item: ShopItem) => {
        if (!user || user.total_xp < item.price) {
            alert('XP가 부족합니다!')
            return
        }

        if (!confirm(`${item.name}을(를) ${item.price} XP에 구매하시겠습니까?`)) return

        try {
            setPurchaseLoading(item.id)
            await api.post(`/shop/purchase/${item.id}`)
            alert('구매가 완료되었습니다!')
            await fetchUser() // XP 갱신
            // TODO: 인벤토리로 이동하시겠습니까? 묻거나...
        } catch (error: any) {
            alert(error.response?.data?.detail || '구매에 실패했습니다.')
        } finally {
            setPurchaseLoading(null)
        }
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">상점</h1>
                    <p className="text-gray-600">XP를 모아 멋진 아이템을 구매하세요!</p>
                </div>
                <div className="flex items-center gap-4">
                    <div className="bg-amber-100 text-amber-800 px-4 py-2 rounded-full font-bold">
                        💰 {user?.total_xp.toLocaleString()} XP
                    </div>
                    <Link
                        to="/inventory"
                        className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                    >
                        🎒 내 인벤토리
                    </Link>
                </div>
            </div>

            {loading ? (
                <div className="flex justify-center py-20">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500" />
                </div>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {items.map((item) => (
                        <motion.div
                            key={item.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
                        >
                            <div className="aspect-square bg-gray-50 relative group">
                                {item.image_url ? (
                                    <img
                                        src={item.image_url}
                                        alt={item.name}
                                        className="w-full h-full object-cover"
                                    />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center text-4xl">
                                        {item.type === 'avatar' ? '👤' : '🎨'}
                                    </div>
                                )}
                                <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                    <span className="text-white font-medium">{item.type}</span>
                                </div>
                            </div>

                            <div className="p-4">
                                <h3 className="font-bold text-gray-900 mb-1">{item.name}</h3>
                                <p className="text-sm text-gray-500 mb-4 h-10 line-clamp-2">
                                    {item.description || '설명이 없습니다.'}
                                </p>

                                <button
                                    onClick={() => handlePurchase(item)}
                                    disabled={purchaseLoading === item.id || (user?.total_xp || 0) < item.price}
                                    className={`w-full py-2.5 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors ${(user?.total_xp || 0) >= item.price
                                            ? 'bg-primary-500 text-white hover:bg-primary-600'
                                            : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                        }`}
                                >
                                    {purchaseLoading === item.id ? (
                                        <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                                    ) : (
                                        <>
                                            <span>{item.price.toLocaleString()} XP</span>
                                        </>
                                    )}
                                </button>
                            </div>
                        </motion.div>
                    ))}
                </div>
            )}
        </div>
    )
}
