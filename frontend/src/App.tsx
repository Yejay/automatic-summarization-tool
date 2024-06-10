// import React, { useState, useRef } from 'react';
// import './App.css';

// function App() {
// 	const [summary, setSummary] = useState<string>('');
// 	const [model, setModel] = useState<string>('bart');
// 	const [loading, setLoading] = useState<boolean>(false);
// 	const [maxLength, setMaxLength] = useState<number>(512);
// 	const [minLength, setMinLength] = useState<number>(30);
// 	const fileInput = useRef<HTMLInputElement>(null);

// 	const handleSubmit = async (event: React.FormEvent) => {
// 		event.preventDefault();
// 		const file = fileInput.current?.files?.[0];
// 		if (!file) {
// 			return;
// 		}

// 		setLoading(true);
// 		const formData = new FormData();
// 		formData.append('file', file);
// 		formData.append('max_length', maxLength.toString());
// 		formData.append('min_length', minLength.toString());

// 		const endpoint = model === 'bart' ? 'summarize_bart' : model === 'pegasus' ? 'summarize_pegasus' : 'summarize_openai';

// 		const response = await fetch(`http://localhost:5000/${endpoint}`, {
// 			method: 'POST',
// 			body: formData,
// 		});

// 		const data = await response.json();
// 		setSummary(data.summary);
// 		setLoading(false);
// 	};

// 	const handleDelete = () => {
// 		setSummary('');
// 	};

// 	return (
// 		<>
// 			<h1>Zusammenfassen</h1>
// 			<div>
// 				<form onSubmit={handleSubmit}>
// 					<input type='file' id='fileInput' ref={fileInput} />
// 					<select value={model} onChange={(e) => setModel(e.target.value)}>
// 						<option value='bart'>BART</option>
// 						<option value='pegasus'>Pegasus</option>
// 						<option value='openai'>OpenAI</option>
// 					</select>
// 					<div>
// 						<label>
// 							Max Length: {maxLength}
// 							<input type='range' min='50' max='1024' value={maxLength} onChange={(e) => setMaxLength(Number(e.target.value))} />
// 						</label>
// 					</div>
// 					<div>
// 						<label>
// 							Min Length: {minLength}
// 							<input type='range' min='10' max='500' value={minLength} onChange={(e) => setMinLength(Number(e.target.value))} />
// 						</label>
// 					</div>
// 					<button type='submit'>Summarize</button>
// 				</form>
// 				{loading && <div className='spinner'></div>}
// 				<div id='summary'>
// 					<h2>Summary</h2>
// 					<p id='summaryText'>{summary}</p>
// 				</div>
// 				<button id='deleteButton' onClick={handleDelete}>
// 					Delete Summary
// 				</button>
// 			</div>
// 		</>
// 	);
// }

// export default App;

import React, { useState, useRef } from 'react';
import './App.css';

function App() {
    const [summary, setSummary] = useState<string>('');
    const [model, setModel] = useState<string>('bart');
    const [loading, setLoading] = useState<boolean>(false);
    const [maxLength, setMaxLength] = useState<number>(512);
    const [minLength, setMinLength] = useState<number>(30);
    const fileInput = useRef<HTMLInputElement>(null);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        const file = fileInput.current?.files?.[0];
        if (!file) {
            return;
        }

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        formData.append('max_length', maxLength.toString());
        formData.append('min_length', minLength.toString());

        const endpoint = model === 'bart' ? 'summarize_bart' : model === 'pegasus' ? 'summarize_pegasus' : 'summarize_openai';

        const response = await fetch(`http://localhost:5000/${endpoint}`, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();
        setSummary(data.summary);
        setLoading(false);
    };

    const handleDelete = () => {
        setSummary('');
    };

    const handleTestEval = async () => {
        setLoading(true);
        const response = await fetch(`http://localhost:5000/test_eval_wip?model=${model}`);
        const data = await response.json();
        setSummary(data.summary);
        setLoading(false);
    };

    return (
        <>
            <h1>Zusammenfassen</h1>
            <div>
                <form onSubmit={handleSubmit}>
                    <input type='file' id='fileInput' ref={fileInput} />
                    <select value={model} onChange={(e) => setModel(e.target.value)}>
                        <option value='bart'>BART</option>
                        <option value='pegasus'>Pegasus</option>
                        <option value='openai'>OpenAI</option>
                    </select>
                    <div>
                        <label>
                            Max Length: {maxLength}
                            <input type='range' min='50' max='1024' value={maxLength} onChange={(e) => setMaxLength(Number(e.target.value))} />
                        </label>
                    </div>
                    <div>
                        <label>
                            Min Length: {minLength}
                            <input type='range' min='10' max='500' value={minLength} onChange={(e) => setMinLength(Number(e.target.value))} />
                        </label>
                    </div>
                    <button type='submit'>Summarize</button>
                </form>
                {loading && <div className='spinner'></div>}
                <div id='summary'>
                    <h2>Summary</h2>
                    <p id='summaryText'>{summary}</p>
                </div>
                <button id='deleteButton' onClick={handleDelete}>
                    Delete Summary
                </button>
                <button id='testEvalButton' onClick={handleTestEval}>
                    TEST EVAL WIP
                </button>
            </div>
        </>
    );
}

export default App;