import InputForm from './components/InputForm.jsx'
import ClubList from './components/ClubList.jsx'
import { useState, useEffect } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE

function App() {
  const [records, setRecords] = useState([])
  const [clubs, setClubs] = useState([])
  const [selectedClub, setSelectedClub] = useState('1W')

   const fetchClubs = async () => {
    const res = await fetch(`${API_BASE}/clubs`)
    const data = await res.json()
    setClubs(data)
  }

  const fetchHistory = async () => {
    const res = await fetch(`${API_BASE}/history`)
    const data = await res.json()
    setRecords(data)
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetchClubs/fetchHistoryは非同期関数内でsetStateしており、同期呼び出しではない（eslint-plugin-react-hooks 7.0.1の既知の誤検知）
    fetchClubs()
    fetchHistory()
  }, [])

  const handleDelete = async (id) => {
    await fetch(`${API_BASE}/history/${id}`, { method: 'DELETE' })
    fetchHistory()
  }

  const handleDeleteAll = async (clubName) => {
    const targets = records.filter((r) => r.club_name === clubName)
    await Promise.all(
      targets.map((r) => fetch(`${API_BASE}/history/${r.id}`, { method: 'DELETE' }))
    )
    fetchHistory()
  }

  return (
    <div>
      <h1>クラブ飛距離メモ</h1>
      <InputForm
        onSave={fetchHistory}
        selectedClub={selectedClub}
        onClubChange={(club) => { setSelectedClub(club) }}
        clubs={clubs}
      />
      <ClubList
        records={records}
        clubs={clubs}
        selectedClub={selectedClub}
        onDelete={handleDelete}
        onDeleteAll={handleDeleteAll}
      />
    </div>
  )

}

export default App