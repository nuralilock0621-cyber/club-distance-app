import { useState } from 'react'
import HistoryRow from './HistoryRow.jsx'

function ClubRow({ selectedClub, average, neighbors, records, onDelete, onDeleteAll }) {
  const [isOpen, setIsOpen] = useState(false)
  const clubRecords = records.filter((r) => r.club_name === selectedClub)

  return (
    <div className="result-card">
      <div className="club-average">
        <span className="club-name">{selectedClub}</span>
        <span className="avg-number">{average}</span>
        <span className="avg-unit">yds avg</span>
      </div>
      <div className="neighbor-list">
        {neighbors.map((n) => (
          <div key={n.club} className="neighbor-row">
            <span className="neighbor-name">{n.club}</span>
            <span className="neighbor-avg">{n.avg} yds</span>
            <span className={n.diff >= 0 ? 'neighbor-diff-plus' : 'neighbor-diff-minus'}>
              {n.diff > 0 ? '+' : ''}{n.diff} yds
            </span>
          </div>
        ))}
      </div>
      <button className="history-toggle" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? '履歴を閉じる' : '履歴を見る'}
      </button>
      {isOpen && (
        <>
          {clubRecords.map((record, index) => (
            <HistoryRow key={record.id} record={record} strokeNumber={index + 1} onDelete={onDelete} />
          ))}
          <div className="delete-all-wrap">
            <button className="delete-all-btn" onClick={() => onDeleteAll(selectedClub)}>まとめて削除</button>
          </div>
        </>
      )}
    </div>
  )
}

export default ClubRow