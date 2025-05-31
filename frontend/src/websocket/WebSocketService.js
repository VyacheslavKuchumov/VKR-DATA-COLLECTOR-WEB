class WebSocketService {
  /**
   * @param {string} jobId – the UUID of the job you’re subscribing to
   */
  constructor(jobId) {
    this.jobId = jobId;
    this.url = `${process.env.VUE_APP_SERVER.replace(/\/+$/,"")}/ws/${jobId}`;
    this.socket = null;
    this.forcedClose = false;
    this.reconnectInterval = 5000;
    this.maxReconnectInterval = 30000;
    this.reconnectDecay = 1.5;
    this.timeoutId = null;
    this.customOnClose = null;
    this.customOnMessage = null;
  }

  async connect() {
    this.forcedClose = false;
    this.socket = new WebSocket(this.url);

    return new Promise((resolve, reject) => {
      this.socket.onopen = () => {
        console.log(`[WS][${this.jobId}] opened`);
        this.reconnectInterval = 5000;
        resolve();
      };

      this.socket.onerror = (err) => {
        console.error(`[WS][${this.jobId}] error:`, err);
      };

      this.socket.onmessage = (event) => {
        if (typeof this.customOnMessage === 'function') {
          this.customOnMessage(event.data);
        } else {
          console.log(`[WS][${this.jobId}] message:`, event.data);
        }
      };

      this.socket.onclose = (evt) => {
        console.log(`[WS][${this.jobId}] closed`, evt);
        if (typeof this.customOnClose === 'function') {
          this.customOnClose(evt);
        }
        if (!this.forcedClose) {
          this.timeoutId = setTimeout(() => {
            this.reconnectInterval = Math.min(
              this.reconnectInterval * this.reconnectDecay,
              this.maxReconnectInterval
            );
            console.log(`[WS][${this.jobId}] reconnect in ${this.reconnectInterval}ms`);
            this.connect();
          }, this.reconnectInterval);
        }
      };
    });
  }

  /**
   * Register a handler for incoming messages (log lines)
   * @param {function(string)} callback 
   */
  onMessage(callback) {
    this.customOnMessage = callback;
  }

  /**
   * Register a handler for socket close events
   * @param {function} callback 
   */
  onClose(callback) {
    this.customOnClose = callback;
  }

  /**
   * Close the socket and stop reconnection attempts
   */
  disconnect() {
    this.forcedClose = true;
    if (this.timeoutId) clearTimeout(this.timeoutId);
    if (this.socket) {
      this.socket.close();
      console.log(`[WS][${this.jobId}] forced close`);
    }
  }
}

export default WebSocketService;
