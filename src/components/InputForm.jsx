import { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE

function InputForm({ onSave, selectedClub, onClubChange, clubs }) {

    const [distance, setDistance] = useState('')
    const handleSave = async () => {
        
        if(distance === ''){
            alert ("数値を入力してください")
            return
        } else if(isNaN(distance)) {
            alert ("数値を入力してください")
            return
        } else if(Number(distance) <= 0) {
            alert ("ミスショットは打ち直してください")
            return
        }

        const club = clubs.find((c) => c.name === selectedClub)

        try {
            const res = await fetch(`${API_BASE}/history`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    clubId: club.id,
                    distance: Number(distance),
                    date: new Date().toISOString().slice(0, 10)
                })
            })

            if (!res.ok) {
                alert('保存に失敗しました')
                return
            }

            setDistance('')
            onSave()
        } catch (err) {
            console.error(err)
            alert('保存に失敗しました')
        }
    
    }

    const handleClubChange = (e) => {
        onClubChange(e.target.value)
    }

    return (
        <div className="input-card">
            <div className="input-row">
                <select value={selectedClub} onChange={handleClubChange}>
	                {clubs.map((club) => (
  				        <option key={club.id} value={club.name}>{club.name}</option>
			        ))}
                </select>
                <input type="number" value={distance} onChange={(e) => setDistance(e.target.value)}>
                </input>
                <button onClick={handleSave}>保存</button>
                
            </div>
        </div>
    )
}



export default InputForm