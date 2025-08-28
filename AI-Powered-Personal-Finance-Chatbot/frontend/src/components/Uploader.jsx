import React, { useState } from 'react'

export default function Uploader({ onUploaded }) {
  const [file, setFile] = useState(null)
  const [msg, setMsg] = useState('')

  const submit = async () => {
    if (!file) return
    setMsg('Uploading… 0%')

    const fd = new FormData()
    fd.append('file', file)

    try {
      const xhr = new XMLHttpRequest()
      xhr.open('POST', 'http://localhost:8000/upload_csv', true)

      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
          const percent = Math.round((event.loaded * 100) / event.total)
          setMsg(`Uploading… ${percent}%`)
        }
      }

      xhr.onload = () => {
        if (xhr.status === 200) {
          const res = JSON.parse(xhr.responseText)
          if (res.ok) {
            setMsg(`Uploaded ${res.rows} rows.`)
            // This line calls the 'refresh' function from the parent App component
            onUploaded?.()
          } else {
            setMsg(res.error || 'Upload failed')
          }
        } else {
          setMsg(`Upload failed: ${xhr.statusText}`)
        }
      }

      xhr.onerror = () => setMsg('Upload failed due to network error')
      xhr.send(fd)
    } catch (err) {
      setMsg(err.message || 'Upload failed')
    }
  }

  return (
    <div style={{ border: '1px solid #eee', padding: 16, borderRadius: 12, margin: '16px 0' }}>
      <input type="file" accept=".csv" onChange={e => setFile(e.target.files?.[0] || null)} />
      <button onClick={submit} style={{ marginLeft: 8 }}>Upload</button>
      <div style={{ marginTop: 8, color: '#555' }}>{msg}</div>
    </div>
  )
}