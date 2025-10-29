import React, { useState } from 'react'

function App() {
    const [inputText, setInputText] = useState('')
    const [outputText, setOutputText] = useState('')

    const convertPunctuation = () => {
        // 、を，に、。を．に変換
        const converted = inputText
            .replace(/、/g, '，')
            .replace(/。/g, '．')
        setOutputText(converted)
    }

    const copyToClipboard = () => {
        navigator.clipboard.writeText(outputText).then(() => {
            alert('コピーしました！')
        })
    }

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <h1>日本語句読点変換ツール</h1>
            <p>日本語の句読点（、。）を全角カンマ・ピリオド（，．）に変換します。</p>

            <div style={{ marginBottom: '20px' }}>
                <h2>入力</h2>
                <textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="ここにテキストを入力してください。"
                    style={{
                        width: '100%',
                        height: '150px',
                        padding: '10px',
                        fontSize: '16px',
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                        resize: 'vertical'
                    }}
                />
            </div>

            <div style={{ marginBottom: '20px', textAlign: 'center' }}>
                <button
                    onClick={convertPunctuation}
                    style={{
                        padding: '10px 30px',
                        fontSize: '16px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer'
                    }}
                    onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#0056b3'}
                    onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#007bff'}
                >
                    変換
                </button>
            </div>

            <div style={{ marginBottom: '20px' }}>
                <h2>出力</h2>
                <textarea
                    value={outputText}
                    readOnly
                    placeholder="変換結果がここに表示されます．"
                    style={{
                        width: '100%',
                        height: '150px',
                        padding: '10px',
                        fontSize: '16px',
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                        backgroundColor: '#f5f5f5',
                        resize: 'vertical'
                    }}
                />
            </div>

            <div style={{ textAlign: 'center' }}>
                <button
                    onClick={copyToClipboard}
                    disabled={!outputText}
                    style={{
                        padding: '10px 30px',
                        fontSize: '16px',
                        backgroundColor: outputText ? '#28a745' : '#ccc',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: outputText ? 'pointer' : 'not-allowed'
                    }}
                    onMouseOver={(e) => {
                        if (outputText) e.currentTarget.style.backgroundColor = '#218838'
                    }}
                    onMouseOut={(e) => {
                        if (outputText) e.currentTarget.style.backgroundColor = '#28a745'
                    }}
                >
                    コピー
                </button>
            </div>
        </div>
    )
}

export default App
