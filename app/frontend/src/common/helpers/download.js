export function triggerDownload (blob, fileName, container) {
  const tempEl = document.createElement('a')
  container.appendChild(tempEl)
  tempEl.style.display = 'none !important'
  const blobUrl = window.URL.createObjectURL(blob)
  tempEl.href = blobUrl
  tempEl.download = fileName
  tempEl.click()
  window.URL.revokeObjectURL(blobUrl)
  setTimeout(() => container.removeChild(tempEl), 100)
}
