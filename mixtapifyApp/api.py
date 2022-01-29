#!/usr/bin/env python3

import spotipy
#from spotipy.oauth2 import SpotifyClientCredentials
class SpotifyClientCredentials(SpotifyAuthBase):
		OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
	
		def __init__(
				self,
				client_id="beea5cbf7cf04684b8738e20fbfe4bad",
				client_secret="e8151b0d0ffa430f824eaa57fdcdad7e",
				proxies=None,
				requests_session=True,
				requests_timeout=None,
				cache_handler=None
		):
				"""
				Creates a Client Credentials Flow Manager.

				The Client Credentials flow is used in server-to-server authentication.
				Only endpoints that do not access user information can be accessed.
				This means that endpoints that require authorization scopes cannot be accessed.
				The advantage, however, of this authorization flow is that it does not require any
				user interaction

				You can either provide a client_id and client_secret to the
				constructor or set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
				environment variables

				Parameters:
							* client_id: Must be supplied or set as environment variable
							* client_secret: Must be supplied or set as environment variable
							* proxies: Optional, proxy for the requests library to route through
							* requests_session: A Requests session
							* requests_timeout: Optional, tell Requests to stop waiting for a response after
																	a given number of seconds
							* cache_handler: An instance of the `CacheHandler` class to handle
															getting and saving cached authorization tokens.
															Optional, will otherwise use `CacheFileHandler`.
															(takes precedence over `cache_path` and `username`)

				"""
			
				super(SpotifyClientCredentials, self).__init__(requests_session)
			
				self.client_id = client_id
				self.client_secret = client_secret
				self.proxies = proxies
				self.requests_timeout = requests_timeout
				if cache_handler:
						assert issubclass(cache_handler.__class__, CacheHandler), \
								"cache_handler must be a subclass of CacheHandler: " + str(type(cache_handler)) \
								+ " != " + str(CacheHandler)
						self.cache_handler = cache_handler
				else:
						self.cache_handler = CacheFileHandler()
					
		def get_access_token(self, as_dict=True, check_cache=True):
				"""
				If a valid access token is in memory, returns it
				Else feches a new token and returns it

						Parameters:
						- as_dict - a boolean indicating if returning the access token
								as a token_info dictionary, otherwise it will be returned
								as a string.
				"""
				if as_dict:
						warnings.warn(
								"You're using 'as_dict = True'."
								"get_access_token will return the token string directly in future "
								"versions. Please adjust your code accordingly, or use "
								"get_cached_token instead.",
								DeprecationWarning,
								stacklevel=2,
						)
					
				if check_cache:
						token_info = self.cache_handler.get_cached_token()
						if token_info and not self.is_token_expired(token_info):
								return token_info if as_dict else token_info["access_token"]
					
				token_info = self._request_access_token()
				token_info = self._add_custom_values_to_token_info(token_info)
				self.cache_handler.save_token_to_cache(token_info)
				return token_info if as_dict else token_info["access_token"]
	
		def _request_access_token(self):
				"""Gets client credentials access token """
				payload = {"grant_type": "client_credentials"}
			
				headers = _make_authorization_headers(
						self.client_id, self.client_secret
				)
			
				logger.debug(
						"sending POST request to %s with Headers: %s and Body: %r",
						self.OAUTH_TOKEN_URL, headers, payload
				)
			
				try:
						response = self._session.post(
								self.OAUTH_TOKEN_URL,
								data=payload,
								headers=headers,
								verify=True,
								proxies=self.proxies,
								timeout=self.requests_timeout,
						)
						response.raise_for_status()
						token_info = response.json()
						return token_info
				except requests.exceptions.HTTPError as http_error:
						self._handle_oauth_error(http_error)
					
		def _add_custom_values_to_token_info(self, token_info):
				"""
				Store some values that aren't directly provided by a Web API
				response.
				"""
				token_info["expires_at"] = int(time.time()) + token_info["expires_in"]
				return token_info
	
birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
	results = spotify.next(results)
	albums.extend(results['items'])
	
for album in albums:
	print(album['name'])