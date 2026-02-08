import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import { Link } from 'react-router-dom'

interface InventoryItem {
    user_item_id: string
    id: string // item_id
    name: string
    type: string
    image_url: string
    is_equipped: boolean
}

export function InventoryPage() {
    const [items, setItems] = useState<InventoryItem[]>([])
    const [loading, setLoading] = useState(true)
    const [actionLoading, setActionLoading] = useState<string | null>(null)

    const fetchInventory = async () => {
        try {
            const { data } = await api.get('/shop/inventory')
            setItems(data.data)
        } catch (error) {
            console.error('Failed to fetch inventory:', error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchInventory()
    }, [])

    const handleEquip = async (item: InventoryItem) => {
        try {
            setActionLoading(item.user_item_id)
            if (item.is_equipped) {
                // 이미 장착 중이면 해제? (API에 unequip이 있는 경우)
                // 현재 API는 equip/unequip 분리됨
                await api.post(`/shop/unequip/${item.id}`) // 주의: API가 item_id를 받는지 user_item_id를 받는지 확인 필요. backend api 코드를 보면 item_id를 받음.
            } else {
                await api.post(`/shop/equip/${item.id}`)
            }

            // 목록 갱신 (단순 토글보다 다시 불러오는게 안전, type별 해제 로직 등 때문)
            await fetchInventory()
        } catch (error: any) {
            alert(error.response?.data?.detail || '작업에 실패했습니다.')
        } finally {
            setActionLoading(null)
        }
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">내 인벤토리</h1>
                    <p className="text-gray-600">구매한 아이템을 장착해보세요!</p>
                </div>
                <div className="flex items-center gap-4">
                    <Link
                        to="/shop"
                        className="px-4 py-2 bg-primary-50 text-primary-600 font-medium rounded-lg hover:bg-primary-100"
                    >
                        🏪 상점으로 가기
                    </Link>
                </div>
            </div>

            {loading ? (
                <div className="flex justify-center py-20">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500" />
                </div>
            ) : items.length === 0 ? (
                <div className="text-center py-20 bg-gray-50 rounded-2xl border border-gray-100">
                    <p className="text-gray-500 mb-4">보유한 아이템이 없습니다.</p>
                    <Link
                        to="/shop"
                        className="inline-block px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 font-bold"
                    >
                        상점 구경하기
                    </Link>
                </div>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {items.map((item) => (
                        <motion.div
                            key={item.user_item_id}
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className={`bg-white rounded-xl shadow-sm border overflow-hidden relative ${item.is_equipped ? 'border-primary-500 ring-2 ring-primary-100' : 'border-gray-100'
                                }`}
                        >
                            {item.is_equipped && (
                                <div className="absolute top-2 right-2 z-10 bg-primary-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                                    장착 중
                                </div>
                            )}

                            <div className="aspect-square bg-gray-50 relative">
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
                            </div>

                            <div className="p-4">
                                <h3 className="font-bold text-gray-900 mb-1">{item.name}</h3>
                                <p className="text-xs text-gray-500 mb-4 uppercase tracking-wider">{item.type}</p>

                                <button
                                    onClick={() => handleEquip(item)}
                                    disabled={actionLoading === item.user_item_id}
                                    className={`w-full py-2 rounded-lg font-bold text-sm transition-colors ${item.is_equipped
                                        ? 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                        : 'bg-primary-500 text-white hover:bg-primary-600'
                                        }`}
                                >
                                    {actionLoading === item.user_item_id ? (
                                        '처리 중...'
                                    ) : item.is_equipped ? (
                                        '장착 해제'
                                    ) : (
                                        '장착하기'
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
