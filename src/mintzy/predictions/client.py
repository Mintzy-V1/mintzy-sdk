from typing import List, Union, Dict, Any, Tuple, Generator
import json
from datetime import datetime
import httpx

from mintzy.predictions.constants import SUPPORTED_TICKERS
from mintzy.models.prediction import PredictionResponse, PredictionRow, PredictionEvent
from mintzy.exceptions import MintzyValidationError

class PredictionClient:
    """Client for interacting with Mintzy prediction endpoints."""
    
    def __init__(self, request_func):
        self._request = request_func

    def _parse_response(self, response_json: Dict[str, Any], tickers: List[str], parameters: List[str]) -> Tuple[Dict[str, List[Dict[str, Any]]], List[str]]:
        parsed = {}
        warnings = []
        if not isinstance(response_json, dict):
            warnings.append(f"Unexpected response type: {type(response_json)}")
            return parsed, warnings
            
        result = response_json.get("result", response_json)
        
        for ticker in tickers:
            ticker_data = result.get(ticker) if isinstance(result, dict) else None
            if ticker_data is None:
                warnings.append(f"No data returned for {ticker}")
                continue
                
            if isinstance(ticker_data, str):
                warnings.append(f"{ticker}: server error — {ticker_data}")
                continue
                
            ticker_rows = []
            
            for param in parameters:
                param_data = ticker_data.get(param) if isinstance(ticker_data, dict) else None
                if param_data is None:
                    warnings.append(f"{param} data missing for {ticker}")
                    continue
                    
                if isinstance(param_data, dict):
                    timestamps = param_data.get("timestamps", [])
                    predicted_prices = param_data.get("predicted_prices", [])
                    dates = param_data.get("dates", [])
                    times = param_data.get("times", [])
                    
                    if not predicted_prices:
                        warnings.append(f"Empty prediction data for {ticker}.{param}")
                        continue
                        
                    for i, price in enumerate(predicted_prices):
                        if price is None:
                            price = 0.0
                            
                        if i < len(timestamps):
                            ts_str = str(timestamps[i])
                            try:
                                dt = datetime.fromisoformat(ts_str)
                                date_str = dt.strftime("%Y-%m-%d")
                                time_str = dt.strftime("%H:%M:%S")
                            except Exception:
                                date_str = str(dates[i]) if i < len(dates) else ts_str
                                time_str = str(times[i]) if i < len(times) else ""
                        else:
                            date_str = str(dates[i]) if i < len(dates) else ""
                            time_str = str(times[i]) if i < len(times) else ""
                            
                        ticker_rows.append({
                            "Ticker": ticker,
                            "Date": date_str,
                            "Time": time_str,
                            "Predicted_Price": float(price),
                        })
                        
                elif isinstance(param_data, str):
                    for line in param_data.strip().split("\n")[1:]:
                        parts = line.split()
                        if len(parts) >= 3:
                            ticker_rows.append({
                                "Ticker": ticker,
                                "Date": parts[0],
                                "Time": parts[1],
                                "Predicted_Price": float(parts[2]),
                            })
                            
                elif isinstance(param_data, list):
                    for i, price in enumerate(param_data):
                        if price is None:
                            continue
                        ticker_rows.append({
                            "Ticker": ticker,
                            "Date": "",
                            "Time": f"slot_{i}",
                            "Predicted_Price": float(price),
                        })
                else:
                    warnings.append(f"Unsupported payload type for {ticker}.{param}: {type(param_data)}")
                    
            if ticker_rows:
                parsed[ticker] = ticker_rows
            else:
                warnings.append(f"No valid rows parsed for {ticker}")
                
        return parsed, warnings

    def get_prediction(self, tickers: Union[str, List[str]], time_frame: str, parameters: Union[str, List[str]], candle: str = "1m") -> PredictionResponse:
        """
        Get predictions for the given tickers.
        
        Args:
            tickers: A single ticker or list of tickers.
            time_frame: Time frame for the prediction (e.g., '20 minutes').
            parameters: A single parameter or list of parameters (e.g., 'close').
            candle: Candle size (e.g., '1m', '5m').
            
        Returns:
            PredictionResponse containing the prediction data.
        """
        if isinstance(tickers, str):
            tickers = [tickers]
        if not isinstance(tickers, list):
            raise MintzyValidationError("Tickers must be a string or list", 400)
            
        invalid = [t for t in tickers if t.upper() not in SUPPORTED_TICKERS]
        if invalid:
            raise MintzyValidationError(f"Ticker(s) not supported currently: {', '.join(invalid)}", 400)
            
        tickers = [t.upper() for t in tickers]
        
        if isinstance(parameters, str):
            parameters = [parameters]
            
        payload = {
            "action": {
                "action_type": "predict",
                "predict": {
                    "given": {
                        "ticker": tickers,
                        "time_frame": time_frame,
                        "candle": candle,
                    },
                    "required": {"parameters": parameters},
                },
            }
        }
        
        response = self._request("POST", "/api/stock/prediction", json=payload)
        response_json = response.json()
        
        parsed, warnings = self._parse_response(response_json, tickers, parameters)
        
        data = []
        for ticker_rows in parsed.values():
            for row in ticker_rows:
                data.append(PredictionRow(**row))
                
        credits = self.get_credits()
                
        return PredictionResponse(
            success=True,
            data=data,
            credits_remaining=credits,
            timestamp=datetime.now().isoformat()
        )

    def stream_prediction_events(self, tickers: Union[str, List[str]], time_frame: str, parameters: Union[str, List[str]], candle: str = "1m") -> Generator[PredictionEvent, None, None]:
        """
        Stream prediction events for the given tickers.
        
        Args:
            tickers: A single ticker or list of tickers.
            time_frame: Time frame for the prediction (e.g., '20 minutes').
            parameters: A single parameter or list of parameters (e.g., 'close').
            candle: Candle size (e.g., '1m', '5m').
            
        Yields:
            PredictionEvent objects containing updates as they stream in.
        """
        if isinstance(tickers, str):
            tickers = [tickers]
        if not isinstance(tickers, list):
            yield PredictionEvent(type="error", status="error", message="Tickers must be a string or list")
            return
            
        invalid = [t for t in tickers if t.upper() not in SUPPORTED_TICKERS]
        if invalid:
            yield PredictionEvent(type="error", status="error", message=f"Ticker(s) not supported currently: {', '.join(invalid)}")
            return
            
        tickers = [t.upper() for t in tickers]
        
        if isinstance(parameters, str):
            parameters = [parameters]
            
        payload = {
            "action": {
                "action_type": "predict",
                "predict": {
                    "given": {
                        "ticker": tickers,
                        "time_frame": time_frame,
                        "candle": candle,
                    },
                    "required": {"parameters": parameters},
                },
            }
        }
        
        processed = []
        
        client = getattr(self, "_httpx_client", None)
        if not client:
            raise RuntimeError("Streaming requires the httpx.Client instance to be available")
            
        base_url = str(client.base_url).rstrip("/")
        stream_url = "/api/stock/prediction/stream" # VERIFY: assumed path
        
        try:
            with client.stream("POST", stream_url, json=payload) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if not line:
                        continue
                        
                    event_dict = json.loads(line)
                    
                    if event_dict.get("type") == "ticker":
                        ticker = event_dict.get("ticker")
                        result = event_dict.get("result")
                        
                        if ticker and event_dict.get("status") == "success":
                            parsed, warnings = self._parse_response({"result": {ticker: result}}, [ticker], parameters)
                            rows = parsed.get(ticker, [])
                            event_dict["predictions"] = [{"Ticker": ticker, **r} for r in rows]
                            event_dict["warnings"] = warnings
                            processed.append(ticker)
                            
                    if event_dict.get("type") == "done":
                        credits = self.get_credits()
                        event_dict["credits_remaining"] = credits
                        event_dict["tickers_processed"] = processed
                        
                    yield PredictionEvent(**event_dict)
                    
        except httpx.TimeoutException:
            yield PredictionEvent(type="error", status="error", message="Request timed out. Please try again.")
        except httpx.RequestError as e:
            yield PredictionEvent(type="error", status="error", message=f"API request failed: {str(e)}")
        except Exception as e:
            yield PredictionEvent(type="error", status="error", message=f"Unexpected error: {str(e)}")
            
    def get_credits(self) -> int:
        """
        Get remaining credits for the user.
        
        Returns:
            Remaining credits as an integer.
        """
        response = self._request("GET", "/api/user/credits") # VERIFY: confirm credits endpoint
        return response.json().get("credits", 0)
