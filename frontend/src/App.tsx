import React, { useState, useRef } from 'react';
import './App.css';

interface EvaluationResult {
	study_id: string;
	scores: {
		bart: { rouge1: number[]; rouge2: number[]; rougeL: number[]; bertscore: number[] };
		pegasus: { rouge1: number[]; rouge2: number[]; rougeL: number[]; bertscore: number[] };
		openai: { rouge1: number[]; rouge2: number[]; rougeL: number[]; bertscore: number[] };
	};
}

function App() {
	const [summary, setSummary] = useState<string>('');
	const [model, setModel] = useState<string>('bart');
	const [loadingSummarize, setLoadingSummarize] = useState<boolean>(false);
	const [loadingEvaluate, setLoadingEvaluate] = useState<boolean>(false);
	const [evaluationResults, setEvaluationResults] = useState<EvaluationResult[] | null>(null);
	const [dragActive, setDragActive] = useState<boolean>(false);
	const [fileName, setFileName] = useState<string | null>(null);
	const fileInput = useRef<HTMLInputElement>(null);

	const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
		e.preventDefault();
		e.stopPropagation();
		if (e.type === 'dragenter' || e.type === 'dragover') {
			setDragActive(true);
		} else if (e.type === 'dragleave') {
			setDragActive(false);
		}
	};

	const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
		e.preventDefault();
		e.stopPropagation();
		setDragActive(false);
		if (e.dataTransfer.files && e.dataTransfer.files[0]) {
			fileInput.current!.files = e.dataTransfer.files;
			setFileName(e.dataTransfer.files[0].name);
		}
	};

	const handleFileInputClick = () => {
		fileInput.current!.click();
	};

	const handleFileChange = () => {
		if (fileInput.current?.files && fileInput.current.files[0]) {
			setFileName(fileInput.current.files[0].name);
		}
	};

	const handleSubmit = async (event: React.FormEvent) => {
		event.preventDefault();
		const file = fileInput.current?.files?.[0];
		if (!file) {
			return;
		}

		setLoadingSummarize(true);
		const formData = new FormData();
		formData.append('file', file);

		const endpoint = model === 'bart' ? 'summarize_bart' : model === 'pegasus' ? 'summarize_pegasus' : 'summarize_openai';

		const response = await fetch(`http://localhost:5000/${endpoint}`, {
			method: 'POST',
			body: formData,
		});

		const data = await response.json();
		setSummary(data.summary);
		setLoadingSummarize(false);
	};

	const handleDelete = () => {
		setSummary('');
	};

	const handleEvaluation = async () => {
		setLoadingEvaluate(true);
		const response = await fetch('http://localhost:5000/evaluate_summaries', {
			method: 'POST',
		});
		const data: EvaluationResult[] = await response.json();
		setEvaluationResults(data);
		setLoadingEvaluate(false);
	};

	const formatScores = (scores: number[] | undefined) => {
		if (!scores || scores.length !== 3) {
			console.error('Scores array is undefined, null, or has incorrect length:', scores);
			return <div>Unavailable</div>;
		}

		return (
			<div>
				<div>Precision: {scores[0].toFixed(3)}</div>
				<div>Recall: {scores[1].toFixed(3)}</div>
				<div>F1: {scores[2].toFixed(3)}</div>
			</div>
		);
	};

	return (
		<div id='root'>
			<h1>Automatic Summarization Tool</h1>
			<div className='card'>
				<h2>Please select a file or drag and drop</h2>
				<div
					className={`file-upload ${dragActive ? 'drag-active' : ''}`}
					onDragEnter={handleDrag}
					onDragLeave={handleDrag}
					onDragOver={handleDrag}
					onDrop={handleDrop}
					onClick={handleFileInputClick}
				>
					<input type='file' id='fileInput' ref={fileInput} onChange={handleFileChange} style={{ display: 'none' }} />
					{fileName ? <p>{fileName}</p> : <p>Drag & Drop your file here or click to upload</p>}
				</div>
				<h2>Please select a model</h2>
				<div style={{ display: 'flex', justifyContent: 'space-between', margin: '10px 0' }}>
					<button onClick={() => setModel('bart')} style={{ flex: 1, margin: '0 25px', backgroundColor: model === 'bart' ? '#646cffaa' : '#333333' }}>
						BART
					</button>
					<button onClick={() => setModel('pegasus')} style={{ flex: 1, margin: '0 25px', backgroundColor: model === 'pegasus' ? '#646cffaa' : '#333333' }}>
						PEGASUS
					</button>
					<button onClick={() => setModel('openai')} style={{ flex: 1, margin: '0 25px', backgroundColor: model === 'openai' ? '#646cffaa' : '#333333' }}>
						GPT
					</button>
				</div>
				<div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px', marginTop: '20px' }}>
					<button onClick={handleSubmit} style={{ width: '25%', padding: '10px', backgroundColor: '#646cffaa', border: 'none', borderRadius: '5px' }}>
						Summarize
					</button>
					{loadingSummarize && <div className='spinner'></div>}
					{summary && (
						<div style={{ marginTop: '20px', backgroundColor: '#333333', padding: '10px', borderRadius: '8px' }}>
							<h2>Summary</h2>
							<p>{summary}</p>
							<button onClick={handleDelete} style={{ backgroundColor: '#960202', border: 'none', borderRadius: '5px' }}>
								Delete Summary
							</button>
						</div>
					)}
					<div className='divider'></div>
					<h2>Understanding ROUGE and BERTScore Metrics</h2>
					<p>
						ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a set of metrics for evaluating automatic summarization and machine translation. Below is a brief explanation of
						what each ROUGE score indicates:
					</p>
					<ul>
						<li>
							<strong>ROUGE-1</strong>: Measures the overlap of unigrams (single words) between the system and reference summaries. Higher values indicate better performance.
						</li>
						<li>
							<strong>ROUGE-2</strong>: Measures the overlap of bigrams (two consecutive words) between the system and reference summaries. Higher values indicate better performance.
						</li>
						<li>
							<strong>ROUGE-L</strong>: Measures the longest common subsequence (LCS) between the system and reference summaries. Higher values indicate better performance.
						</li>
					</ul>
					<h2>BERTScore Metrics</h2>
					<p>
						BERTScore evaluates text generation based on semantic similarity using BERT embeddings. Higher values indicate better semantic similarity.
					</p>
					<button onClick={handleEvaluation} style={{ width: '25%', padding: '10px', backgroundColor: '#646cffaa', border: 'none', borderRadius: '5px' }}>
						Evaluate Summaries
					</button>
					{loadingEvaluate && <div className='spinner'></div>}
				</div>
				{evaluationResults && (
					<div style={{ marginTop: '20px' }}>
						<h2>Evaluation Metrics</h2>
						<table className='styled-table'>
							<thead>
								<tr>
									<th>Study ID</th>
									<th>Model</th>
									<th>ROUGE-1</th>
									<th>ROUGE-2</th>
									<th>ROUGE-L</th>
									<th>BERTScore</th>
								</tr>
							</thead>
							<tbody>
								{evaluationResults.map((result) => (
									<React.Fragment key={result.study_id}>
										<tr>
											<td rowSpan={3}>{result.study_id}</td>
											<td>BART</td>
											<td>{formatScores(result.scores.bart.rouge1)}</td>
											<td>{formatScores(result.scores.bart.rouge2)}</td>
											<td>{formatScores(result.scores.bart.rougeL)}</td>
											<td>{formatScores(result.scores.bart.bertscore)}</td>
										</tr>
										<tr>
											<td>PEGASUS</td>
											<td>{formatScores(result.scores.pegasus.rouge1)}</td>
											<td>{formatScores(result.scores.pegasus.rouge2)}</td>
											<td>{formatScores(result.scores.pegasus.rougeL)}</td>
											<td>{formatScores(result.scores.pegasus.bertscore)}</td>
										</tr>
										<tr>
											<td>OpenAI</td>
											<td>{formatScores(result.scores.openai.rouge1)}</td>
											<td>{formatScores(result.scores.openai.rouge2)}</td>
											<td>{formatScores(result.scores.openai.rougeL)}</td>
											<td>{formatScores(result.scores.openai.bertscore)}</td>
										</tr>
									</React.Fragment>
								))}
							</tbody>
						</table>
					</div>
				)}
			</div>
		</div>
	);
}

export default App;

