function LoadingStatus({content}) {
    return <div className="loading-container">
        <h2>Generating {content}</h2>

        <div className="loading-animation">
            <div className="spinner"></div>
        </div>

        <p className="loading-info">
            Please wait while we generate your data.
        </p>
    </div>
}

export default LoadingStatus;